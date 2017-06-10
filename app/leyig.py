# coding: utf-8
import ConfigParser
import os

from botocore.config import Config
import json, time
import boto3
import base64
import hashlib
import hmac
from django.core.serializers.json import DjangoJSONEncoder

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class LeYig(object):
    YIG_ENDPOINT = ""
    YIG_ACCESSKEYID = ""
    YIG_SECRETACCESSKEY = ""
    YIG_BUCKET = ""
    YIG_REGION = ''

    def __init__(self, endpoint=YIG_ENDPOINT, accesskeyId=YIG_ACCESSKEYID, secretaccesskey=YIG_SECRETACCESSKEY,
                 region=YIG_REGION, bucket=YIG_BUCKET):
        self.endpoint = endpoint
        self.accesskeyId = accesskeyId
        self.secretaccesskey = secretaccesskey
        self.region = region
        self.bucket = bucket
        self.client = self.connect()

        # self.bucket = self.client.Bucket(self.bucketname)

    def get_configs(self, path):
        if path:
            config = ConfigParser.ConfigParser()
            config.read(path)
            self.endpoint = config.get('yig', 'endpoint')
            self.accesskeyId = config.get('yig', 'accessKeyId')
            self.secretaccesskey = config.get('yig', 'secretAccessKey')
            self.region = config.get('yig', 'region')
            self.client = self.connect()

    def getObjectByBucket(self, bucketname=YIG_BUCKET):
        print json.dumps(self.client.list_objects(Bucket=bucketname), cls=DjangoJSONEncoder)

    def getSignPutUrl(self, key, bucketname=YIG_BUCKET):
        key = key.strip()
        conditions = [
            {'bucket': bucketname},
            {"acl": "public-read"},
            ["eq", "$Key", key],
            ["starts-with", "$Content-Type", "text"],
        ]
        print conditions

        print key
        return self.client.generate_presigned_post(bucketname, key, {}, conditions, ExpiresIn=3600)

    def getDownUrl(self, key, bucketname=YIG_BUCKET):
        return self.client.generate_presigned_url('get_object', {'Bucket': bucketname, 'Key': key}, 7*24*60*60, 'GET')

    def getPublicUrl(self, key, bucketname=YIG_BUCKET):
        return self.getDownUrl(key, bucketname).split('?', 1)[0]

    def connect(self):
        reconfig = Config(signature_version="s3", region_name='cn-north-1')
        s3 = boto3.client('s3', use_ssl=True, verify=None, endpoint_url=self.endpoint,
                          aws_access_key_id=self.accesskeyId, aws_secret_access_key=self.secretaccesskey,
                          config=reconfig)
        return s3

    def upload_url(self, base_dir, *args):
        timestamp = str(int(time.time()))
        result = {}
        for f in args:
            self.client.upload_file(base_dir+f, self.bucket, timestamp+f)
            url = self.getDownUrl(timestamp+f)
            result[f] = url
        return result
            

if __name__ == '__main__':
    yig = LeYig()
    # yig.getObjectByBucket()
    # print json.dumps(yig.getDownUrl('testfile.txt'))
    # print json.dumps(yig.getSignPutUrl('123.txt'))
    print "================================"
    timestamp = str(int(time.time()))
    resopn = yig.client.upload_file(BASE_DIR+"/app/static/satabw_iops.log-lat.png", 'perf', timestamp+'lat.png')
    
    # url = yig.getDownUrl(timestamp+'lat.png', bucketname='perf')
    # url = yig.getDownUrl('1496389426lat.png', bucketname='perf')
    res = yig.upload_url(BASE_DIR+'/app/static/', 'satabw_iops.log-lat.png', 'satabw_iops.log-slat.png')
    print res
