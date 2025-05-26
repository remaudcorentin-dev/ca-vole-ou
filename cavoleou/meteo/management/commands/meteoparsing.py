
from django.core.management.base import BaseCommand

from datetime import datetime, timedelta

from meteo.models import Spot, Meteo

from meteo.meteo_parsing.provider.wrf import extract
from meteo.meteo_parsing.upsert import meteo_data_to_models


class Command(BaseCommand):
    help = "Run to retrieve, parse and store weather data"

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        for spot in Spot.objects.all():
            meteo_data = extract(spot.meteo_url, spot.name)
            meteo_data_to_models(meteo_data, spot)

        # Remove "old" weather data
        Meteo.objects.filter(datetime__lt=datetime.now() - timedelta(hours=6)).delete()
