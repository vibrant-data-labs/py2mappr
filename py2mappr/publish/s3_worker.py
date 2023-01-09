import configparser
import os
from typing import Dict
from pathlib import Path
import boto3


def has_google_analytics(data: str) -> bool:
    return "googletagmanager.com" in data


def has_publish_tags(data: str) -> bool:
    return "<title>openmappr | network exploration tool</title>" not in data


def s3_worker(path: Path, bucket_name: str):
    _file_mapping: Dict[str, str] = {
        "html": "text/html",
        "json": "application/json",
        "sh": "text/x-shellscript",
        "png": "image/png",
        "jpg": "image/jpeg",
        "jpeg": "image/jpeg",
        "gif": "image/gif",
        "svg": "image/svg+xml",
    }
    ### Config Setup ###
    config = configparser.ConfigParser()
    wd = Path.cwd()
    configpath = wd / "config.ini"
    config.read(configpath)
    # load AWS settings from config file
    REGION = config["aws"]["region"]
    ACCESS_KEY = config["aws"]["access_key_id"]
    SECRET_KEY = config["aws"]["secret_access_key"]
    S3_CLIENT = boto3.client(
        "s3",
        aws_access_key_id=ACCESS_KEY,
        aws_secret_access_key=SECRET_KEY,
        region_name=REGION,
    )
    # create public bucket if it doesn't exist
    S3_CLIENT.create_bucket(Bucket=bucket_name, ACL="public-read")

    # Create the configuration for the website
    website_configuration = {
        "ErrorDocument": {"Key": "error.html"},
        "IndexDocument": {"Suffix": "index.html"},
    }
    # Set the new policy on the selected bucket
    S3_CLIENT.put_bucket_website(
        Bucket=bucket_name, WebsiteConfiguration=website_configuration
    )

    session = boto3.Session(
        aws_access_key_id=ACCESS_KEY,
        aws_secret_access_key=SECRET_KEY,
        region_name=REGION,
    )
    s3 = session.resource("s3")
    bucket = s3.Bucket(bucket_name)

    has_index = False
    try:
        S3_CLIENT.head_object(Bucket=bucket_name, Key="index.html")
        has_index = True
    except:
        has_index = False
        pass

    data_path = str(path)
    for subdir, _, files in os.walk(path):
        for file in files:
            full_path = os.path.join(subdir, file)
            with open(full_path, "rb") as data:
                ext = full_path.split(".")[-1]
                object_key = (
                    full_path[len(data_path) + 1 :]
                    if subdir == data_path
                    else "%s/%s"
                    % (os.path.basename(subdir), os.path.basename(full_path))
                )

                if has_index and ("index.html" in str(full_path)):
                    print("index.html found")
                    with open(full_path, "r") as f:
                        html_text = f.read()
                    checks = [has_publish_tags, has_google_analytics]

                    if all([check(html_text) for check in checks]):
                        print("Skipping index.html")
                        continue

                print(f"Putting {object_key} to {bucket_name}")
                bucket.put_object(
                    Key=object_key,
                    Body=data,
                    ACL="public-read",
                    ContentType=_file_mapping[ext],
                )

    print(
        "\nUpload complete. To view your map, go to http://%s.s3-website-%s.amazonaws.com/"
        % (bucket_name, REGION)
    )

    return {"bucket": bucket_name, "region": REGION}
