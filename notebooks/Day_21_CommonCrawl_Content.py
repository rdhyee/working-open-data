# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <markdowncell>

# Although we're putting a lot of emphasis in WwOD on doing the basic task of counting files and bytes in Common Crawl, this notebook will show you how to look at the *content* of the files in Common Crawl.  

# <headingcell level=1>

# Setup

# <codecell>

# http://boto.s3.amazonaws.com/s3_tut.html

import boto
from boto.s3.connection import S3Connection

from itertools import islice

conn = S3Connection()

# turns out there is an anonymous mode in boto for public data sets:
# https://github.com/keiw/common_crawl_index/commit/ad341d0a41a828f260c9c08419dadff0dac6cf5b#L0R33
#conn=S3Connection(anon=True)

bucket = conn.get_bucket('aws-publicdatasets')

# <headingcell level=1>

# Integration with url index

# <markdowncell>

# Look at http://urlsearch.commoncrawl.org/
# 
# * [blog post about URL search](http://commoncrawl.org/url-search-tool/)
# * [blog post about the URL search index](http://commoncrawl.org/common-crawl-url-index/)

# <markdowncell>

# For example, let's look up ischool.berkeley.edu in the URL index:
# 
# http://urlsearch.commoncrawl.org/?q=ischool.berkeley.edu
# 
# You can also download the results as a json file 
# 
# http://urlsearch.commoncrawl.org/download?q=edu.berkeley.ischool
# 
# which can be parsed:

# <codecell>

import requests
import json
s = requests.get("http://urlsearch.commoncrawl.org/download?q=edu.berkeley.ischool")
data = [json.loads(row) for row in s.content.split("\n") if row]
print len(data)

# <codecell>

# http://urlsearch.commoncrawl.org/page/1346876860493/1346901517112/422/320051/596
u = data[0]
u

# <codecell>

# form the urlsearch url from the information returned
urlsearch_url = "http://urlsearch.commoncrawl.org/page/{arcSourceSegmentId}/{arcFileDate}/{arcFileParition}/{arcFileOffset}/{compressedSize}".format(**u)
urlsearch_url

# <codecell>

# can also look up the corresponding arc.gz file in S3

!s3cmd ls s3://aws-publicdatasets/common-crawl/parse-output/segment/1346876860493/1346901517112_422.arc.gz 

# <headingcell level=1>

# Grabbing pieces of the .arc.gz files

# <markdowncell>

# I think it's possible to use the Python module [warc](https://github.com/internetarchive/warc/blob/master/docs/index.rst) to parse out the .arc.gz files but if we have the offset and size (provided by the URL index), we don't have to grab the entire file -- but just the piece we want.

# <markdowncell>

# **Range** specification in S3
# 
# http://docs.aws.amazon.com/AmazonS3/latest/API/RESTObjectGET.html  ->  Downloads the specified range bytes of an object. For more information about the HTTP Range header, go to http://www.w3.org/Protocols/rfc2616/rfc2616-sec14.html#sec14.35
# 
# try: 
# 
# bytes={offset}-499
# 
# 
# OK -- the offset and compressed size can still be used even with gzip compression -- see https://github.com/trivio/common_crawl_index#retrieving-a-page
# 

# <codecell>

#https://github.com/trivio/common_crawl_index#retrieving-a-page

from StringIO import StringIO
from gzip import GzipFile


def arc_file(s3, bucket, info):

    bucket = s3.lookup(bucket)
    keyname = "/common-crawl/parse-output/segment/{arcSourceSegmentId}/{arcFileDate}_{arcFileParition}.arc.gz".format(**info)
    key = bucket.lookup(keyname)
    
    start = info['arcFileOffset']
    end = start + info['compressedSize'] - 1
    
    headers={'Range' : 'bytes={}-{}'.format(start, end)}
    
    chunk = StringIO(
         key.get_contents_as_string(headers=headers)
    )
    
    return GzipFile(fileobj=chunk).read()

# <codecell>

u

# <codecell>

s = arc_file(conn, 'aws-publicdatasets', u)

# <codecell>

# voila

print s

# <headingcell level=1>

# Parsing the metadata and textdata files

# <markdowncell>

# Where to go next:  tempting to go implement the index crawling described in:
# 
# http://commoncrawl.org/common-crawl-url-index/
# 
# index itself:  The index itself is located public datasets bucket at s3://aws-publicdatasets/common-crawl/projects/url-index/url-index.1356128792.
# 
# Lot more to explore at https://github.com/trivio/common_crawl_index

# <headingcell level=1>

# metadata and text files

# <codecell>

# example -- let's look at a the structure of a metadata file
# grab 'common-crawl/parse-output/segment/1346823845675/metadata-00000'

k = bucket.get_key('common-crawl/parse-output/segment/1346823845675/metadata-00000')
k.size

# <markdowncell>

# public URLs -- don't need to generate signature: https://aws-publicdatasets.s3.amazonaws.com/common-crawl/parse-output/segment/1346823845675/metadata-00000

# <codecell>

# easiest way to get file into the local directory -- warning file size is 41857708

!wget https://aws-publicdatasets.s3.amazonaws.com/common-crawl/parse-output/segment/1346823845675/metadata-00000

# <codecell>

# alternative -- use boto to download to local file -- this method will be useful if you want grab content from S3
fp = open('metadata-00000', 'wb')
k.get_file(fp)
fp.close()

# <markdowncell>

# The metadata and textdata files in Common Crawl are [Hadoop sequences files](http://wiki.apache.org/hadoop/SequenceFile), specifically, https://github.com/matteobertozzi/Hadoop/blob/master/python-hadoop/examples/SequenceFileReader.py.  To parse them, we will use library from https://github.com/matteobertozzi/Hadoop -- here are some installation instructions.  (I've installed these libraries on the PiCloud `rdhyee/Working_with_Open_Data` environment
# 
#     git clone git://github.com/matteobertozzi/Hadoop.git
#     cd Hadoop/python-hadoop
#     python setup.py install
# 
# 

# <codecell>

import sys
import json
from hadoop.io import SequenceFile
from itertools import islice


def SequenceFileIterator(path):
    reader = SequenceFile.Reader(path)

    key_class = reader.getKeyClass()
    value_class = reader.getValueClass()

    key = key_class()
    value = value_class()

    position = reader.getPosition()

    while reader.next(key, value):
        yield (position, key.toString(), value.toString())
        position = reader.getPosition()

    reader.close()    
    

path = "metadata-00000"

# read parts of the metdata-0000 file 
for (i, (pos, k, v)) in enumerate(islice(SequenceFileIterator(path), 1)):
    v = json.loads(v)
    archiveInfo = v.get('archiveInfo', None)
    print i, k, archiveInfo
    print "metadata available:", v.keys()
    

# <codecell>


