import configparser
from pathlib import Path
from typing import TypedDict
import boto3
import time


def cloudfront_worker(bucket: str, url: str):
    ### Config Setup ###
    config = configparser.ConfigParser()
    wd = Path.cwd()
    configpath = wd / "config.ini"
    config.read(configpath)
    # load AWS settings from config file
    REGION = config["aws"]["region"]
    ACCESS_KEY = config["aws"]["access_key_id"]
    SECRET_KEY = config["aws"]["secret_access_key"]
    ACM_CERTIFICATE = config["aws"]["acm_certificate"]
    bucket_website = "%s.s3-website-%s.amazonaws.com" % (bucket, REGION)
    print(f"Publishing to Cloudfront: {url}, bucket: {bucket_website}")

    CLOUDFRONT_CLIENT = boto3.client(
        "cloudfront",
        aws_access_key_id=ACCESS_KEY,
        aws_secret_access_key=SECRET_KEY,
        region_name=REGION,
    )

    # ensure distribution is not created already
    distributions = CLOUDFRONT_CLIENT.list_distributions()
    for distribution in distributions["DistributionList"]["Items"]:
        if (
            distribution["Aliases"]["Items"][0] == url
            and distribution["Origins"]["Items"][0]["DomainName"]
            == bucket_website
        ):
            print("Distribution already exists, skipping")
            return {"cdn_url": distribution.get("DomainName")}

    response = CLOUDFRONT_CLIENT.create_distribution(
        DistributionConfig={
            "Origins": {
                "Quantity": 1,
                "Items": [
                    {
                        "DomainName": bucket_website,
                        "Id": bucket_website,
                        "CustomOriginConfig": {
                            "HTTPPort": 80,
                            "HTTPSPort": 443,
                            "OriginProtocolPolicy": "http-only",
                            "OriginSslProtocols": {
                                "Quantity": 3,
                                "Items": ["TLSv1", "TLSv1.1", "TLSv1.2"],
                            },
                            "OriginReadTimeout": 30,
                            "OriginKeepaliveTimeout": 5,
                        },
                    }
                ],
            },
            "Aliases": {"Quantity": 1, "Items": [url]},
            "ViewerCertificate": {
                "SSLSupportMethod": "sni-only",
                "ACMCertificateArn": ACM_CERTIFICATE,
            },
            "DefaultCacheBehavior": {
                "TargetOriginId": bucket_website,
                "ViewerProtocolPolicy": "redirect-to-https",
                "MinTTL": 0,
                "DefaultTTL": 128,
                "MaxTTL": 256,
                "ForwardedValues": {
                    "QueryString": False,
                    "Cookies": {"Forward": "none"},
                    "Headers": {"Quantity": 0},
                },
            },
            "Comment": "",
            "Enabled": True,
            "CallerReference": str(time.time()).replace(".", ""),
        }
    )

    print(
        "Distribution created: %s"
        % response.get("Distribution").get("DomainName")
    )
    return {"cdn_url": response.get("Distribution").get("DomainName")}
