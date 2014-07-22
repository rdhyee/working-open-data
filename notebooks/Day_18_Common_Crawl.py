# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <markdowncell>

# installing [s3cmd](http://s3tools.org/s3cmd):
# 
#     pip install s3cmd
# 

# <codecell>

!s3cmd ls s3://aws-publicdatasets/common-crawl/parse-output/valid_segments.txt

# <codecell>

# http://boto.s3.amazonaws.com/s3_tut.html

import boto
from boto.s3.connection import S3Connection

from itertools import islice

# public bucket
conn = S3Connection()
bucket = conn.get_bucket('aws-publicdatasets')
for key in islice(bucket.list(prefix="common-crawl/parse-output/", delimiter="/"),None):
    print key.name.encode('utf-8')

# <codecell>

# get valid_segments
import boto
from boto.s3.connection import S3Connection

conn = S3Connection()
bucket = conn.get_bucket('aws-publicdatasets')

k = bucket.get_key("common-crawl/parse-output/valid_segments.txt")
s = k.get_contents_as_string()

# <codecell>

len(s.split("\n"))

# <codecell>

s.split("\n")

# <codecell>

# what to do with a valid segment instance?
# https://groups.google.com/forum/#!msg/common-crawl/QYTmnttZZyo/NPiXvK8ZeiMJ

