import os
import pandas as pd

from .patterns import download_pattern, ip_pattern, date_pattern
from .config import load_config
from .ip_lookup import get_ip_info


def parse_logs(folder, geolocate=True, config_path=None):

    rows = []

    current_date = None
    current_ip = None
    current_country = None
    current_city = None
    current_org = None
    current_lat = None
    current_lon = None

    DATA_FORMATS, SYSTEM_ENDPOINTS = load_config(config_path)

    files = [f for f in os.listdir(folder) if f.startswith("log")]

    for file in files:

        path = os.path.join(folder, file)

        if not os.path.isfile(path):
            continue

        with open(path, "r", errors="ignore") as f:

            for line in f:

                if line.startswith("{{{{#"):
                    current_date = None
                    current_ip = None
                    current_country = None
                    current_city = None
                    current_org = None
                    current_lat = None
                    current_lon = None

                date_match = date_pattern.search(line)
                if date_match:
                    current_date = date_match.group(0)

                if geolocate:
                    
                    ip_match = ip_pattern.search(line)

                    if ip_match:

                        current_ip = ip_match.group(1)
                        info = get_ip_info(current_ip)

                        current_country = info["country"]
                        current_city = info["city"]
                        current_org = info["org"]
                        current_lat = info["lat"]
                        current_lon = info["lon"]

                m = download_pattern.search(line)

                if m:

                    dataset = m.group(2)

                    if dataset in SYSTEM_ENDPOINTS:
                        continue

                    fmt = m.group(3)

                    row = {
                        "type": "download" if fmt in DATA_FORMATS else "view",
                        "dataset": dataset,
                        "format": fmt,
                        "date": current_date
                    }

                    if geolocate:
                        row.update({
                            "ip": current_ip,
                            "country": current_country,
                            "city": current_city,
                            "org": current_org,
                            "lat": current_lat,
                            "lon": current_lon
                        })

                    rows.append(row)

    df = pd.DataFrame(rows)

    df["date"] = pd.to_datetime(df["date"], utc=True).dt.tz_localize(None)

    total_downloads = (df["type"] == "download").sum()
    total_views = (df["type"] == "view").sum()

    return df, total_views, total_downloads