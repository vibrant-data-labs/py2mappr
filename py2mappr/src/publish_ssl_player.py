import boto3
import sys
import configparser
import pathlib as pl
import time
import requests

### Config Setup ###
config = configparser.ConfigParser()
wd = pl.Path.cwd() 
configpath = wd/'config.ini'
config.read(configpath)

# load AWS settings from config file
REGION = config['aws']['region']
ACCESS_KEY = config['aws']['access_key_id']
SECRET_KEY = config['aws']['secret_access_key']
ACM_CERTIFICATE = config['aws']['acm_certificate']
# load Cloudflare settings from config file
CF_API_KEY=config['cloudflare']['api_key']
CF_ID=config['cloudflare']['id']

CLOUDFRONT_CLIENT = boto3.client(
                        'cloudfront',
                        aws_access_key_id=ACCESS_KEY,
                        aws_secret_access_key=SECRET_KEY,
                        region_name=REGION
                        )

PLAYER_DISTRIBUTION = 'mappr-player.openmappr.org'

def create_distribution(bucket, url):
  bucket_website = 'http://%s.s3-website-%s.amazonaws.com'% (bucket, REGION)
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
      'TargetOriginId': '%s.s3-website-%s.amazonaws.com'% (bucket, REGION),
      'ViewerProtocolPolicy': 'redirect-to-https'
    },
    'Comment': '',
    'Enabled': True,
    'CallerReference': str(time.time()).replace('.', '')
  })

  return response.get('Distribution')

def add_cloudflare_cname(cloudfront_url, url):
  auth_header = {
    'Authorization': 'Bearer %s'%CF_API_KEY
  }
  cf_zone = requests.get('https://api.cloudflare.com/client/v4/zones', headers = auth_header)

  zone_name ='.'.join(url.split('.')[-2:])
  domain = list(filter(lambda zone: zone.get('name') == zone_name, cf_zone.json().get('result')))
  if (len(domain) == 0):
    print('No zones found bound to %s'%zone_name)
    return

  domain_item = domain[0]
  
  data = {
    'type': 'CNAME',
    'name': url,
    'content': cloudfront_url,
    'ttl': 1
  }
  requests.post('https://api.cloudflare.com/client/v4/zones/%s/dns_records'%domain_item.get('id'), headers = auth_header, json = data)

  print('https://%s is created'%url)

if __name__ == "__main__":
  args = sys.argv
  if len(args) < 3:
    print('Pass a valid bucket name: publish_ssl_player.py my-bucket name.domain.com')
    sys.exit(1)

  bucket_name = args[1]
  url = args[2]
  distribution = create_distribution(bucket_name, url) # e.g. "mymap.openmappr.org" (no https://)
  add_cloudflare_cname(distribution.get('DomainName'), url) # note 'DomainName' is fixed

