import boto
import boto.s3
import os
from lib.weekday import get_previous_weekday

def upload_csv(csv):
    AWS_ACCESS_KEY_ID = os.environ['AWS_ACCESS_KEY_ID']
    AWS_SECRET_ACCESS_KEY = os.environ['AWS_SECRET_ACCESS_KEY']
    AWS_REGION_HOST = os.environ['AWS_S3_REGION_HOST']

    # https://docs.aws.amazon.com/general/latest/gr/rande.html
    conn = boto.connect_s3(AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, host=AWS_REGION_HOST)
    filename = '{}.csv'.format(get_previous_weekday())
    bucket = conn.get_bucket('daily-stock-data')
    key = boto.s3.key.Key(bucket, filename)
    key.set_contents_from_string(csv)
    key.set_acl('public-read')
    s3_url = 'https://{}/daily-stock-data/{}'.format(AWS_REGION_HOST, filename)
    return s3_url


