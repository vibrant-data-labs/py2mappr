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

def invalidate_cache(distribution):
  CLOUDFRONT_CLIENT.create_invalidation(
    DistributionId=distribution.get('Id'), 
    InvalidationBatch={
      'Paths': {
        'Quantity': 1,
        'Items': ['/*']
      },
      'CallerReference': str(time.time()).replace('.', '')
    })

def purge_cache(bucket_name):
  all_distributions = CLOUDFRONT_CLIENT.list_distributions()
  allowed_origin = '%s.s3-website-%s.amazonaws.com'%(bucket_name, REGION)
  filter_condition = lambda distr: allowed_origin in map(lambda x: x.get('DomainName'),distr.get('Origins').get('Items')) or PLAYER_DISTRIBUTION in distr.get('Aliases').get('Items')
  distributions = list(filter(filter_condition,all_distributions.get('DistributionList').get('Items')))
  print('Found %s distributions'%str(len(distributions)))
  print(','.join(map(lambda d: ''.join(d.get('Aliases').get('Items')), distributions)))
  
  for distr in distributions:
    invalidate_cache(distr)
    alias = ''.join(distr.get('Aliases').get('Items'))
    print('%s invalidated'%alias)
    purge_cloudflare_cache(alias)

def purge_cloudflare_cache(url: str):
  if (not CF_API_KEY):
    return
  
  auth_header = {
    'Authorization': 'Bearer %s'%CF_API_KEY
  }
  cf_zone = requests.get('https://api.cloudflare.com/client/v4/zones', headers = auth_header)

  zone_name ='.'.join(url.split('.')[-2:])
  domain = list(filter(lambda zone: zone.get('name') == zone_name, cf_zone.json().get('result')))
  if (len(domain) == 0):
    return

  domain_item = domain[0]
  purge_data = {
    'files': [url]
  }
  requests.post('https://api.cloudflare.com/client/v4/zones/%s/purge_cache'%domain_item.get('id'), headers = auth_header, json =purge_data)
  print('CloudFlare: %s cache is cleaned'%url)


if __name__ == "__main__":
  args = sys.argv
  if len(args) == 1:
    print('Pass a valid bucket name: purge_cache.py my-bucket')
    sys.exit(1)

  purge_cache(args[1:][0])