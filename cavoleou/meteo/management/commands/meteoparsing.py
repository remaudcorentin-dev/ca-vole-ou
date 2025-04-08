
from django.core.management.base import BaseCommand

from meteo.models import Spot

from meteo.meteo_parsing.provider.wrf import extract
from meteo.meteo_parsing.upsert import meteo_data_to_models


class Command(BaseCommand):
    help = "todo"

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        for spot in Spot.objects.all():
            meteo_data = extract(spot.meteo_url, spot.name)
            meteo_data_to_models(meteo_data, spot)
