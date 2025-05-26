from django.shortcuts import render, get_object_or_404

from datetime import timedelta, time
from collections import defaultdict, OrderedDict
from django.utils.timezone import now
from meteo.models import Spot, Meteo

def get_grouped_meteo_data(one_spot=None):
    current_time = now()
    time_threshold = current_time - timedelta(hours=3)

    result = {}

    if one_spot:
        spots = [one_spot]
    else:
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
                continue
            day_key = dt.date()
            grouped_by_day[day_key].append(meteo)

        result[spot] = [grouped_by_day[day] for day in sorted(grouped_by_day.keys())]

    if one_spot:
        return result[one_spot]

    ordered_result = OrderedDict(
        sorted(result.items(), key=lambda item: item[0].display_order)
    )

    return ordered_result

def home(request):
    context = {
        "grouped_meteo_data": get_grouped_meteo_data()
    }
    return render(request, template_name="home.html", context=context)

def spot_detail(request, spot_id):
    spot = get_object_or_404(Spot, pk=spot_id)

    print(get_grouped_meteo_data(one_spot=spot))

    context = {
        "meteo_data": get_grouped_meteo_data(one_spot=spot),
        "spot": spot,
    }
    return render(request, template_name="spot_detail.html", context=context)
