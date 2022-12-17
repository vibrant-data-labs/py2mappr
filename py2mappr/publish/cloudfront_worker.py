import configparser
from pathlib import Path
import boto3
import time


def cloudfront_worker(bucket: str, url: str):
    ### Config Setup ###
    config = configparser.ConfigParser()
    wd = Path.cwd()
    configpath = wd/'config.ini'
    config.read(configpath)
    # load AWS settings from config file
    REGION = config['aws']['region']
    ACCESS_KEY = config['aws']['access_key_id']
    SECRET_KEY = config['aws']['secret_access_key']
    ACM_CERTIFICATE = config['aws']['acm_certificate']
    bucket_website = 'http://%s.s3-website-%s.amazonaws.com' % (
        bucket, REGION)

    CLOUDFRONT_CLIENT = boto3.client(
        'cloudfront',
        aws_access_key_id=ACCESS_KEY,
        aws_secret_access_key=SECRET_KEY,
        region_name=REGION
    )
    response = CLOUDFRONT_CLIENT.create_distribution(DistributionConfig={
        'Origins': {
            'Quantity': 1,
            'Items': [{
                'Id': bucket_website,
                'DomainName': bucket_website
            }]
        },
        'Aliases': {
            'Quantity': 1,
            'Items': [url]
        },
        'ViewerCertificate': {
            'ACMCertificateArn': ACM_CERTIFICATE
        },
        'DefaultCacheBehavior': {
            'TargetOriginId': '%s.s3-website-%s.amazonaws.com' % (bucket, REGION),
            'ViewerProtocolPolicy': 'redirect-to-https'
        },
        'Comment': '',
        'Enabled': True,
        'CallerReference': str(time.time()).replace('.', '')
    })

    return response.get('Distribution')
