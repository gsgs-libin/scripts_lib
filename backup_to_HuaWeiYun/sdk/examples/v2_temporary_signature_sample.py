#!/usr/bin/python  
# -*- coding:utf-8 -*- 

'''
 This sample demonstrates how to do common operations in v2 temporary signature way
 on Huawei OBS using the OBS SDK for Python.
'''

AK = '*** Provide your Access Key ***'
SK = '*** Provide your Secret Key ***'
server = 'obs.myhwclouds.com'
signature = 'v4'
path_style = True
bucketName = 'my-obs-bucket-demo'
objectKey = 'my-obs-object-key-demo'

import sys, ssl
IS_PYTHON2 = sys.version_info.major == 2 or not sys.version > '3'

if IS_PYTHON2:
    from urlparse import urlparse
    import httplib
else:
    import http.client as httplib
    from urllib.parse import urlparse

from com.obs.client.obs_client import ObsClient
# Constructs a obs client instance with your account for accessing OBS
obsClient = ObsClient(access_key_id=AK, secret_access_key=SK, server=server, signature=signature, path_style=path_style, is_secure=False)

def doAction(msg, method, url, headers=None, content=None):
    print(msg + ' using v2 temporary signature url:')
    print('\t' + url)

    url = urlparse(url)

    if headers is None:
        headers = {}

    conn = httplib.HTTPConnection(url.hostname, url.port)
    path = url.path + '?' + url.query
    conn.request(method, path, headers=headers)

    if content is not None:
        content = content if IS_PYTHON2 else content.encode('UTF-8')
        conn.send(content)

    result = conn.getresponse()
    status = result.status
    responseContent = result.read()
    if status < 300:
        print(msg + ' using v2 temporary signature url successfully.')
    else:
        print(msg + ' using v2 temporary signature url failed!!')

    if responseContent:
        print('\tresponseContent:')
        print('\t%s' % responseContent)
    conn.close()
    print('\n')

# Create bucket
method = 'PUT'
url = obsClient.createV2SignedUrl(method, bucketName, expires= 3600)
doAction('Creating bucket', method, url)

# Set/Get/Delete bucket cors
method = 'PUT'
from com.obs.models.cors_rule import CorsRule
from com.obs.utils import convert_util, common_util
cors1 = CorsRule(id='rule1', allowedMethod=['PUT', 'HEAD', 'GET'],
                 allowedOrigin=['http://www.a.com', 'http://www.b.com'], allowedHeader=['Authorization1'],
                 maxAgeSecond=100, exposeHeader=['x-obs-test1'])
cors2 = CorsRule(id='rule2', allowedMethod=['PUT', 'HEAD', 'GET'],
                 allowedOrigin=['http://www.c.com', 'http://www.d.com'], allowedHeader=['Authorization2'],
                 maxAgeSecond=200, exposeHeader=['x-obs-test2'])
corsList = [cors1, cors2]

content = convert_util.transCorsRuleToXml(corsList)
headers = {'Content-Type': 'application/xml', 'Content-Length': str(len(content)), 'Content-MD5': common_util.base64_encode(common_util.md5_encode(content))}
url = obsClient.createV2SignedUrl(method, bucketName, specialParam='cors', headers=headers)
doAction('Setting bucket cors', method, url, headers, content)

method = 'GET'
url = obsClient.createV2SignedUrl(method, bucketName, specialParam='cors')
doAction('Getting bucket cors', method, url)

method = 'DELETE'
url = obsClient.createV2SignedUrl(method, bucketName, specialParam='cors')
doAction('Deleting bucket cors', method, url)

# Put object
method = 'PUT'
content = 'Hello OBS'
headers = {'Content-Length': str(len(content))}
url = obsClient.createV2SignedUrl(method, bucketName, objectKey, headers=headers)
doAction('Creating object', method, url, headers, content)

# Get object
method = 'GET'
url = obsClient.createV2SignedUrl(method, bucketName, objectKey)
doAction('Getting object', method, url)

# Set/Get object acl
method = 'PUT'
headers = {'x-amz-acl': 'public-read'}
url = obsClient.createV2SignedUrl(method, bucketName, objectKey, specialParam='acl', headers=headers)
doAction('Setting object acl', method, url, headers)

method = 'GET'
url = obsClient.createV2SignedUrl(method, bucketName, objectKey, specialParam='acl')
doAction('Getting object acl', method, url)

# Delete object
method = 'DELETE'
url = obsClient.createV2SignedUrl(method, bucketName, objectKey)
doAction('Deleting object', method, url)

# Delete bucket
method = 'DELETE'
url = obsClient.createV2SignedUrl(method, bucketName, expires=3600)
doAction('Deleting bucket', method, url)
