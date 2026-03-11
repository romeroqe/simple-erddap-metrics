import requests
import time

ip_cache = {}

def get_ip_info(ip):

    if ip in ip_cache:
        return ip_cache[ip]

    try:
        r = requests.get(f"http://ip-api.com/json/{ip}", timeout=5)
        data = r.json()

        info = {
            "country": data.get("country"),
            "city": data.get("city"),
            "org": data.get("org"),
            "lat": data.get("lat"),
            "lon": data.get("lon"),
        }

    except:
        info = dict(country=None, city=None, org=None, lat=None, lon=None)

    ip_cache[ip] = info
    time.sleep(0.05)

    return info