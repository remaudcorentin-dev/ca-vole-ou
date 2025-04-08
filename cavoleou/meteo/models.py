from django.db import models

from meteo.utils import vent_direction_int_to_enum


class Spot(models.Model):
    name = models.CharField(max_length=255)
    meteo_url = models.CharField(max_length=255)
    description = models.TextField()

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

    def __str__(self):
        return f"{self.spot.name} - {self.datetime:%d/%m %Hh} - {self.vent_direction_int_to_enum} {self.vent_moyen_kmh}/{self.vent_rafales_kmh} km/h"
