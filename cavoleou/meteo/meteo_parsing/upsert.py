
from meteo.models import Meteo

def meteo_data_to_models(meteo_data, spot):
    for meteo_row in meteo_data:
        meteo_obj, _ = Meteo.objects.get_or_create(key=meteo_row['key'], spot=spot)
        for key, value in meteo_row.items():
            setattr(meteo_obj, key, value)
        meteo_obj.save()
