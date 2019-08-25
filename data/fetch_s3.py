import json
import os

import boto3


with open('../configs.json') as f:
    configs = json.load(f)

profile_name = configs["aws_profile_name"]
session = boto3.Session(profile_name=profile_name)
s3 = session.resource('s3')

bucket_name = configs["aws_raw_data_bucket_name"]
my_bucket = s3.Bucket(bucket_name)

for s3_object in my_bucket.objects.all():
    # Need to split s3_object.key into path and file name, else it will give
    # error file not found.
    path, filename = os.path.split(s3_object.key)

    if "json" in str(filename):
        # pulling data obtained via, finx-data-catcher
        # https://github.com/westonplatter/finx-data-catcher
        local_filename = f"finx-data-catcher/{path}/{filename}"
        os.makedirs(os.path.dirname(local_filename), exist_ok=True)

        my_bucket.download_file(s3_object.key, local_filename)
        msg = f"downloaded {path}/{filename}"
        print(msg)
