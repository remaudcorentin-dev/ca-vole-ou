from django.db import models

from meteo.utils import vent_direction_int_to_enum

from computedfields.models import ComputedFieldsModel, computed


class Spot(ComputedFieldsModel):
    FLYABILIY_GOOD = "FLYABILIY_GOOD"
    FLYABILIY_LIMIT = "FLYABILIY_LIMIT"
    FLYABILIY_BAD = "FLYABILIY_BAD"

    FLYABILIY_STATUS = (
        (FLYABILIY_GOOD, "Good"),
        (FLYABILIY_LIMIT, "Limit"),
        (FLYABILIY_BAD, "Bad"),
    )

    name = models.CharField(max_length=255)
    meteo_url = models.CharField(max_length=255)

    href_ffvl = models.TextField(blank=True)
    href_club = models.TextField(blank=True)
    href_beacon = models.TextField(blank=True)
    href_map = models.TextField(blank=True)

    description = models.TextField(blank=True)

    min_wind_speed_limit = models.IntegerField(default=10)
    min_wind_speed_good = models.IntegerField(default=15)
    max_wind_speed_good = models.IntegerField(default=20)
    max_wind_speed_limit = models.IntegerField(default=25)

    max_gusts_speed_good = models.IntegerField(default=30)
    max_gusts_speed_limit = models.IntegerField(default=35)

    vent_directions_good = models.JSONField(default=list)

    vent_directions_limit = models.JSONField(default=list)

    def __str__(self):
        return self.name


class Meteo(ComputedFieldsModel):
    key = models.CharField(max_length=255)

    spot = models.ForeignKey(Spot, on_delete=models.CASCADE)

    datetime = models.DateTimeField(null=True)
    temperature = models.IntegerField(null=True)
    vent_direction = models.IntegerField(null=True)
    vent_moyen_kmh = models.IntegerField(null=True)
    vent_rafales_kmh = models.IntegerField(null=True)
    temps = models.CharField(max_length=255, null=True, blank=True)
    pluie = models.FloatField(null=True, default=0)

    @computed(
        models.CharField(max_length=3, null=True, default=None),
        depends=[('self', ['vent_direction'])]
    )
    def vent_direction_int_to_enum(self):
        if not self.vent_direction:
            return None
        return vent_direction_int_to_enum(self.vent_direction)

    @computed(
        models.CharField(max_length=32, default=Spot.FLYABILIY_GOOD),
        depends=[
            ('self', ['vent_moyen_kmh']),
            ('spot', ['min_wind_speed_good', 'max_wind_speed_good', 'min_wind_speed_limit', 'max_wind_speed_limit']),
        ]
    )
    def wind_speed_status(self):
        if not self.vent_moyen_kmh:
            return Spot.FLYABILIY_BAD

        if self.spot.min_wind_speed_good <= self.vent_moyen_kmh <= self.spot.max_wind_speed_good:
            return Spot.FLYABILIY_GOOD
        if self.spot.min_wind_speed_limit <= self.vent_moyen_kmh <= self.spot.max_wind_speed_limit:
            return Spot.FLYABILIY_LIMIT
        return Spot.FLYABILIY_BAD

    @computed(
        models.CharField(max_length=32, default=Spot.FLYABILIY_GOOD),
        depends=[
            ('self', ['vent_rafales_kmh']),
            ('spot', ['max_gusts_speed_good', 'max_gusts_speed_limit']),
        ]
    )
    def gusts_speed_status(self):
        if not self.vent_rafales_kmh:
            return Spot.FLYABILIY_BAD

        if not self.vent_rafales_kmh:
            return Spot.FLYABILIY_BAD
        if self.vent_rafales_kmh <= self.spot.max_gusts_speed_good:
            return Spot.FLYABILIY_GOOD
        if self.vent_rafales_kmh <= self.spot.max_gusts_speed_limit:
            return Spot.FLYABILIY_LIMIT
        return Spot.FLYABILIY_BAD


    @computed(
        models.CharField(max_length=32, default=Spot.FLYABILIY_GOOD),
        depends=[
            ('self', ['vent_direction_int_to_enum']),
            ('spot', ['vent_directions_good', 'vent_directions_limit']),
        ]
    )
    def wind_direction_status(self):
        if not self.vent_direction_int_to_enum:
            return Spot.FLYABILIY_BAD

        if self.vent_direction_int_to_enum in self.spot.vent_directions_good:
            return Spot.FLYABILIY_GOOD
        if self.vent_direction_int_to_enum in self.spot.vent_directions_limit:
            return Spot.FLYABILIY_LIMIT
        return Spot.FLYABILIY_BAD

    @computed(
        models.CharField(max_length=32, default=Spot.FLYABILIY_GOOD),
        depends=[
            ('self', ['pluie']),
        ]
    )
    def weather_status(self):
        if not self.pluie:
            return Spot.FLYABILIY_GOOD
        if float(self.pluie) <= 0:
            return Spot.FLYABILIY_GOOD
        if float(self.pluie) <= 0.2:
            return Spot.FLYABILIY_LIMIT
        return Spot.FLYABILIY_BAD

    def tide_status(self):
        return Spot.FLYABILIY_GOOD  # TODO

    def day_time_status(self):
        return Spot.FLYABILIY_GOOD  # TODO

    @computed(
        models.CharField(max_length=32, default=Spot.FLYABILIY_GOOD),
        depends=[
            ('self', ['wind_speed_status', 'gusts_speed_status', 'wind_direction_status', 'weather_status']),
        ]
    )
    def flyability_status(self):
        if not self.spot:
            return None

        flyability_statuses = (
            self.wind_speed_status,
            self.gusts_speed_status,
            self.wind_direction_status,
            self.weather_status,
            #self.tide_status,
            #self.day_time_status,
        )

        if Spot.FLYABILIY_BAD in flyability_statuses:
            return Spot.FLYABILIY_BAD
        if Spot.FLYABILIY_LIMIT in flyability_statuses:
            return Spot.FLYABILIY_LIMIT
        return Spot.FLYABILIY_GOOD

    def __str__(self):
        return f"{self.spot.name} - {self.datetime:%d/%m %Hh} - {self.vent_direction_int_to_enum} {self.vent_moyen_kmh}/{self.vent_rafales_kmh} km/h -> {self.flyability_status}"
