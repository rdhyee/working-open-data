# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <headingcell level=1>

# Optional:  get s3cmd, boto set up locally

# <markdowncell>

# I have `s3cmd` and `boto` set up on PiCloud's `/rdhyee/Working_with_Open_Data` environment set up.  

# <headingcell level=2>

# You might be having pip problems -- if so....

# <markdowncell>

# consult http://stackoverflow.com/questions/15441224/can-i-relink-enthought-python-to-new-version-of-openssl-on-mac-os-x

# <headingcell level=2>

# s3cmd:  how I installed it

# <markdowncell>

# 
# I used
# https://github.com/s3tools/s3cmd
# 
# how I installed on my notebook:
# 
#     cd ~/C/src/
#     git clone git://github.com/s3tools/s3cmd.git
# 
#     cd s3cmd/
# 
#     python setup.py install
#     s3cmd --configure

# <headingcell level=1>

# Learning about Common Crawl structure

# <codecell>

# s3cmd installed in custom PiCloud environment -- and maybe in your local environment too

!s3cmd ls s3://aws-publicdatasets/common-crawl/parse-output/valid_segments.txt

# <headingcell level=2>

# Reading keys hanging off of s3://aws-publicdatasets/common-crawl/parse-output/

# <codecell>

# http://boto.s3.amazonaws.com/s3_tut.html

import boto
from boto.s3.connection import S3Connection

from itertools import islice

conn = S3Connection()
bucket = conn.get_bucket('aws-publicdatasets')
for key in islice(bucket.list(prefix="common-crawl/parse-output/", delimiter="/"),None):
    print key.name.encode('utf-8')

# <codecell>

# get valid_segments
# https://commoncrawl.atlassian.net/wiki/display/CRWL/About+the+Data+Set

import boto
from boto.s3.connection import S3Connection

conn = S3Connection()
bucket = conn.get_bucket('aws-publicdatasets')

k = bucket.get_key("common-crawl/parse-output/valid_segments.txt")
s = k.get_contents_as_string()

# <codecell>

# how many valid segments in current crawl
len(s.split("\n"))

# <codecell>

valid_segments = s.split("\n")

# <codecell>

# get sample valid segment
valid_segments[0]

# <codecell>

# what to do with a valid segment instance?
# https://groups.google.com/forum/#!msg/common-crawl/QYTmnttZZyo/NPiXvK8ZeiMJ

# <codecell>

# "s3n://aws-publicdatasets/common-crawl/parse-output/segment/"+segmentId+"/*.arc.gz";
!s3cmd ls s3://aws-publicdatasets/common-crawl/parse-output/segment/1346823845675 

# <codecell>

from itertools import islice

conn = S3Connection()
bucket = conn.get_bucket('aws-publicdatasets')
for key in islice(bucket.list(prefix="common-crawl/parse-output/segment/1346823845675/", delimiter="/"),10):
    print key.name.encode('utf-8')

# <codecell>

# WARNING -- this might take a bit of time to run

%time all_files = list(islice(bucket.list(prefix="common-crawl/parse-output/segment/1346823845675/", delimiter="/"),None))

# <codecell>

len(all_files), all_files[0]

# <codecell>

!s3cmd ls s3://aws-publicdatasets/common-crawl/parse-output/segment/1346823845675/1346864466526_10.arc.gz 

# <codecell>

file0 = all_files[0]

# <codecell>

# http://boto.readthedocs.org/en/latest/ref/s3.html#module-boto.s3.key

type(file0), file0.size, file0.content_type

# <codecell>

sum([f.size for f in all_files])

# <codecell>

# estimate of size
len(valid_segments)*__builtin__.sum([f.size for f in all_files])

# <codecell>

all_files[-10:]

# <markdowncell>

# types of files
# 
# * *.arc.gz
# * textData-*
# * metadata-*
# 
# everything belongs into one of those classes?

# <codecell>

from collections import Counter

def cc_file_type(path):

    fname = path.split("/")[-1]
    
    if fname[-7:] == '.arc.gz':
        return 'arc.gz'
    elif fname[:9] == 'textData-':
        return 'textData'
    elif fname[:9] == 'metadata-':
        return 'metadata'
    elif fname == '_SUCCESS':
        return 'success'
    else:
        print path
        return 'other'
    

# <codecell>

Counter([cc_file_type(f.name) for f in all_files])

# <codecell>

all_files[0]

# <headingcell level=1>

# Integration with url index

# <markdowncell>

# http://urlsearch.commoncrawl.org/download?q=edu.berkeley.ischool

# <codecell>

import requests
import json
s = requests.get("http://urlsearch.commoncrawl.org/download?q=edu.berkeley.ischool")
data = [json.loads(row) for row in s.content.split("\n") if row]

# <codecell>

u = data[0]

# <codecell>

# http://urlsearch.commoncrawl.org/page/1346876860493/1346901517112/422/320051/596

# <codecell>

u

# <codecell>

urlsearch_url = "http://urlsearch.commoncrawl.org/page/{arcSourceSegmentId}/{arcFileDate}/{arcFileParition}/{arcFileOffset}/{compressedSize}".format(**u)
urlsearch_url

# <codecell>

!s3cmd ls s3://aws-publicdatasets/common-crawl/parse-output/segment/1346876860493/1346901517112_422.arc.gz 

# <codecell>

# how to grab 320051/596 out of that file?
# hints at https://github.com/trivio/common_crawl_index

