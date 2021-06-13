#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 31 19:39:17 2021

@author: ericberlow
"""
import boto3
import os
import configparser
import pathlib as pl
import reference as ref
import http.server
import socketserver
import webbrowser

### Config Setup ###
config = configparser.ConfigParser()
wd = pl.Path.cwd() 
configpath = wd/'config.ini'
config.read(configpath)
# load AWS settings from config file
REGION = config['aws']['region']
ACCESS_KEY = config['aws']['access_key_id']
SECRET_KEY = config['aws']['secret_access_key']


# launch local server and open browser to display map
def run_local(project_directory, PORT=5000):
    """
    launches a new tab in active browswer with the map
    project_directory : string, the directory with the project data (index.html and 'data' folder)
    """
    web_dir = os.path.join(os.getcwd(), project_directory)
    os.chdir(web_dir)  # change to project directory where index.html and data folder are

    webbrowser.open_new_tab("http://localhost:" + str(PORT))  # open new tab in browswer

    Handler = http.server.SimpleHTTPRequestHandler
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print("\nServing locally at port", PORT, "go to http://localhost:%s \nCTL_C to quit\n" % str(PORT))
        httpd.serve_forever()

def upload_to_s3(path, bucket_name):
    print("\nUploading map to AWS S3 Bucket, named %s, as static website"%bucket_name)
    S3_CLIENT = boto3.client(
                            's3',
                            aws_access_key_id=ACCESS_KEY,
                            aws_secret_access_key=SECRET_KEY,
                            region_name=REGION
                            )   
    # create public bucket if it doesn't exist
    S3_CLIENT.create_bucket(Bucket=bucket_name, ACL='public-read')

    # Create the configuration for the website
    website_configuration = {
        'ErrorDocument': {'Key': 'error.html'},
        'IndexDocument': {'Suffix': 'index.html'},
    }
    # Set the new policy on the selected bucket
    S3_CLIENT.put_bucket_website(
        Bucket=bucket_name,
        WebsiteConfiguration=website_configuration
    )

    session = boto3.Session(
        aws_access_key_id= ACCESS_KEY,
        aws_secret_access_key=SECRET_KEY,
        region_name= REGION
    )
    s3 = session.resource('s3')
    bucket = s3.Bucket(bucket_name)
 
    for subdir, dirs, files in os.walk(path):
        for file in files:
            full_path = os.path.join(subdir, file)
            with open(full_path, 'rb') as data:
                bucket.put_object(Key=full_path[len(path)+1:], Body=data,
                                  ACL='public-read', ContentType=  "text/html")
                
    print("\nView map at http://%s.s3-website-us-east-1.amazonaws.com/"%bucket_name)
 
if __name__ == "__main__":
    
    playerpath = wd/"player" # openmappr files
    player_s3_bucket = "test-openmappr-player"
    #run_local(str(ref.playerpath))
    upload_to_s3(str(playerpath), player_s3_bucket)
    
    

