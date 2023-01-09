import configparser
from pathlib import Path
import requests


def cloudflare_worker(cdn_url: str, url: str):
    print(f"Cloudflare worker: {cdn_url} {url}")
    config = configparser.ConfigParser()
    wd = Path.cwd()
    configpath = wd / "config.ini"
    config.read(configpath)
    CF_API_KEY = config["cloudflare"]["api_key"]
    auth_header = {"Authorization": "Bearer %s" % CF_API_KEY}
    cf_zone = requests.get(
        "https://api.cloudflare.com/client/v4/zones", headers=auth_header
    )

    zone_name = ".".join(url.split(".")[-2:])
    domain = list(
        filter(
            lambda zone: zone.get("name") == zone_name,
            cf_zone.json().get("result"),
        )
    )
    if len(domain) == 0:
        print("No zones found bound to %s" % zone_name)
        return

    domain_item = domain[0]

    data = {"type": "CNAME", "name": url, "content": cdn_url, "ttl": 1, "proxied": True}
    requests.post(
        "https://api.cloudflare.com/client/v4/zones/%s/dns_records"
        % domain_item.get("id"),
        headers=auth_header,
        json=data,
    )

    print("https://%s is created" % url)
