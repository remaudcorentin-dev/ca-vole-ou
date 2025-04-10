from django.shortcuts import render

from datetime import datetime, timedelta, time
from collections import defaultdict
from django.utils.timezone import now
from meteo.models import Spot, Meteo

def get_grouped_meteo_data():
    current_time = now()
    time_threshold = current_time - timedelta(hours=1)

    result = {}

    spots = Spot.objects.all()

    for spot in spots:
        meteos = Meteo.objects.filter(
            spot=spot,
            datetime__gt=time_threshold
        ).order_by('datetime')

        # Group by day
        grouped_by_day = defaultdict(list)
        for meteo in meteos:
            dt = meteo.datetime
            if dt.time() < time(6, 0) or dt.time() > time(22, 0):
                continue  # ignorer les heures hors plage
            day_key = dt.date()
            grouped_by_day[day_key].append(meteo)

        result[spot] = [grouped_by_day[day] for day in sorted(grouped_by_day.keys())]

    return result

def home(request):
    context = {
        "grouped_meteo_data": get_grouped_meteo_data()
    }
    return render(request, template_name="home.html", context=context)
