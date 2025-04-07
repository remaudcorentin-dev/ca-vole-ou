from django.contrib import admin

from meteo.models import Spot


@admin.register(Spot)
class SpotAdmin(admin.ModelAdmin):
    class Meta:
        model = Spot
