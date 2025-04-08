from django.contrib import admin

from meteo.models import Spot, Meteo


@admin.register(Spot)
class SpotAdmin(admin.ModelAdmin):
    class Meta:
        model = Spot


@admin.register(Meteo)
class MeteoAdmin(admin.ModelAdmin):
    class Meta:
        model = Meteo
