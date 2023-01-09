import configparser
from pathlib import Path
import requests


def ec2_worker(bucket: str, url: str, region: str):
    print(f"EC2 worker: {bucket} {url} {region}")
    config = configparser.ConfigParser()
    wd = Path.cwd()
    configpath = wd / "config.ini"
    config.read(configpath)
    API_URL = config["deploy_agent"]["url"]
    API_KEY = config["deploy_agent"]["api_key"]
    auth_header = {"X-Auth": API_KEY}

    data = {"bucket": bucket, "url": url, "region": region}

    requests.post(
        f"{API_URL}/api/project/publish-raw", headers=auth_header, json=data
    )

    print("https://%s is created" % url)
