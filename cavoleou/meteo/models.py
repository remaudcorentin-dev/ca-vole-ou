from django.db import models

from meteo.utils import vent_direction_int_to_enum


class Spot(models.Model):
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
    description = models.TextField()

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


class Meteo(models.Model):
    key = models.CharField(max_length=255)

    spot = models.ForeignKey(Spot, on_delete=models.CASCADE)

    datetime = models.DateTimeField(null=True)
    temperature = models.IntegerField(null=True)
    vent_direction = models.IntegerField(null=True)
    vent_moyen_kmh = models.IntegerField(null=True)
    vent_rafales_kmh = models.IntegerField(null=True)
    temps = models.CharField(max_length=255, null=True, blank=True)

    @property
    def vent_direction_int_to_enum(self):
        return vent_direction_int_to_enum(self.vent_direction)

    @property
    def wind_speed_status(self):
        print(self.spot.min_wind_speed_good, self.vent_moyen_kmh, self.spot.max_wind_speed_good)
        print(self.spot.min_wind_speed_good <= self.vent_moyen_kmh <= self.spot.max_wind_speed_good)
        if self.spot.min_wind_speed_good <= self.vent_moyen_kmh <= self.spot.max_wind_speed_good:
            return Spot.FLYABILIY_GOOD
        if self.spot.min_wind_speed_limit <= self.vent_moyen_kmh <= self.spot.max_wind_speed_limit:
            return Spot.FLYABILIY_LIMIT
        return Spot.FLYABILIY_BAD

    @property
    def gusts_speed_status(self):
        if self.vent_rafales_kmh <= self.spot.max_gusts_speed_good:
            return Spot.FLYABILIY_GOOD
        if self.vent_rafales_kmh <= self.spot.max_gusts_speed_limit:
            return Spot.FLYABILIY_LIMIT
        return Spot.FLYABILIY_BAD

    @property
    def wind_direction_status(self):
        if self.vent_direction_int_to_enum in self.spot.vent_directions_good:
            return Spot.FLYABILIY_GOOD
        if self.vent_direction_int_to_enum in self.spot.vent_directions_limit:
            return Spot.FLYABILIY_LIMIT
        return Spot.FLYABILIY_BAD

    @property
    def weather_status(self):
        return Spot.FLYABILIY_GOOD  # TODO

    @property
    def tide_status(self):
        return Spot.FLYABILIY_GOOD  # TODO

    @property
    def day_time_status(self):
        return Spot.FLYABILIY_GOOD  # TODO

    @property
    def flyability_status(self):
        if not self.spot:
            return None

        flyability_statuses = (
            self.wind_speed_status,
            self.gusts_speed_status,
            self.wind_direction_status,
            self.weather_status,
            self.tide_status,
        )
        print(flyability_statuses)

        if Spot.FLYABILIY_BAD in flyability_statuses:
            return Spot.FLYABILIY_BAD
        if Spot.FLYABILIY_LIMIT in flyability_statuses:
            return Spot.FLYABILIY_LIMIT
        return Spot.FLYABILIY_GOOD

    def __str__(self):
        return f"{self.spot.name} - {self.datetime:%d/%m %Hh} - {self.vent_direction_int_to_enum} {self.vent_moyen_kmh}/{self.vent_rafales_kmh} km/h -> {self.flyability_status}"
