from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import re

import requests

# from meteo.meteo_parsing.provider.wrf import extract ; extract("https://www.meteociel.fr/previsions-wrf-1h/3725/commes.htm", "Commes")



def clean_temperature(text):
    return text.replace("°C", "").strip()

def clean_percentage(text):
    return text.replace("%", "").strip()

def clean_pression(text):
    return text.replace("hPa", "").strip()

def clean_pluie(text):
    if text == "--":
        return "0"
    return text.replace(" mm", "").replace(" cm", "")

def extract_angle(text):
    match = re.search(r"(\d+)\s*°", text)
    return int(match.group(1)) if match else None

def clean_data(forecast_data):
    for entry in forecast_data:
        entry["temperature"] = int(clean_temperature(entry["temperature"]))
        #entry["humidite"] = int(clean_percentage(entry["humidite"]))
        #entry["pression"] = int(clean_pression(entry["pression"]))
        entry["vent_direction"] = int(extract_angle(entry["vent_direction"]))
        entry["pluie"] = float(entry["pluie"])
        entry["vent_moyen_kmh"] = int(entry["vent_moyen_kmh"])
        entry["vent_rafales_kmh"] = int(entry["vent_rafales_kmh"])
    return forecast_data

def clean_temps(text):
    return text.strip()

def extract(url, spot_name):

    html_data = requests.get(url).text
    soup = BeautifulSoup(html_data, "html.parser")

    # tmp
    # spot_name = "Commes"
    # file = "/Users/cremaud/Code/Corem/ca-vole-ou/html-meteo-templates/commes.html"
    # with open(file, "r", encoding="iso-8859-1") as f:
    #     soup = BeautifulSoup(f, "html.parser")
    # endtmp

    # Récupération de toutes les tables
    tables = soup.find_all("table")

    # Recherche de la table contenant les prévisions météo
    target_table = None
    for table in tables:
        if "Jour" in table.get_text() and "Heure" in table.get_text():
            target_table = table
            break

    # Si la table est trouvée, on l'extrait
    forecast_data = []
    if target_table:
        current_date = None
        day_offset = 0
        base_date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)

        rows = target_table.find_all("tr")[2:]  # On saute les lignes d'entête

        for row in rows:
            cols = row.find_all("td")
            if not cols:
                continue

            if "rowspan" in cols[0].attrs:  # Colonne contenant le jour
                jour_texte = cols[0].get_text(strip=True)
                match = re.search(r"([a-zA-Zéû]+)\s*(\d+)", jour_texte)
                if match:
                    current_date = base_date + timedelta(days=day_offset)
                    day_offset += 1
                heure_col = cols[1].get_text(strip=True)
                offset = 2
            else:
                heure_col = cols[0].get_text(strip=True)
                offset = 1

            # Construction du datetime
            try:
                heure = int(heure_col.split(":")[0])
                forecast_datetime = current_date.replace(hour=heure)
            except:
                continue

            try:
                forecast_data.append({
                    "datetime": forecast_datetime.isoformat(),
                    "temperature": cols[offset].get_text(strip=True),
                    # "temp_ressentie": cols[offset + 1].get_text(strip=True),
                    "vent_direction": cols[offset + 2].img['alt'] if cols[offset + 2].find("img") else None,
                    "vent_moyen_kmh": cols[offset + 3].get_text(strip=True),
                    "vent_rafales_kmh": cols[offset + 4].get_text(strip=True),
                    "pluie": clean_pluie(cols[offset + 5].get_text(strip=True)),
                    #"humidite": cols[offset + 6].get_text(strip=True),
                    #"pression": cols[offset + 7].get_text(strip=True),
                    "temps": clean_temps(cols[offset + 8].img['alt']) if cols[offset + 8].find("img") else None,
                    "key": f"WRF-{spot_name}-{forecast_datetime.isoformat()}"
                })
            except Exception as e:
                print(e)

    forecast_data = clean_data(forecast_data)

    print(forecast_data[:5])
    return forecast_data
