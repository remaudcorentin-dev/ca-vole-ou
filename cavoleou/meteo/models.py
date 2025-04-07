from django.db import models


class Spot(models.Model):
    name = models.CharField(max_length=255)
    meteo_url = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.name


class Meteo(models.Model):
    key = models.CharField(max_length=255)

    spot = models.ForeignKey(Spot, on_delete=models.CASCADE)

    datetime = models.DateTimeField()
    temperature = models.IntegerField()
    vent_direction = models.IntegerField()
    vent_moyen_kmh = models.IntegerField()
    vent_rafales_kmh = models.IntegerField()
    temps = models.CharField(max_length=255)
