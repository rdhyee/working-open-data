# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

from __future__ import print_function

# <codecell>

import boto
from boto.s3.connection import S3Connection

from itertools import islice

conn = S3Connection()
bucket = conn.get_bucket('aws-publicdatasets')

# <codecell>

# a function to help with looking through S3 buckets

from itertools import islice

def keys_in_bucket(bucket, prefix, truncate_path=True, limit=None):
    """
    given a S3 boto bucket, yields the keys in bucket with the prefix
    if truncate_path is True, remove prefix in keys
    optional limit to number of keys to return
    """
    keys = islice(bucket.list(prefix=prefix, 
                                   delimiter="/"),
                       limit)
    for key in keys:
        name = key.name.encode("UTF-8") 
        if truncate_path:
            name = name.replace(prefix, "", 1)
        yield name
            

# <headingcell level=1>

# What are the complete range of data for CC?

# <codecell>

# earlier?

!s3cmd ls s3://aws-publicdatasets/common-crawl/

# <codecell>

list(keys_in_bucket(bucket, "common-crawl/"))

# <codecell>

# 2012 data that I was working with in 2013.
# not a good idea to list the folder for "common-crawl/parse-output/segment/"
# instead -- depend on s3://aws-publicdatasets/common-crawl/parse-output/valid_segments.txt

# comment out so I won't run 

# for (i,key) in enumerate(islice(keys_in_bucket(bucket, "common-crawl/parse-output/segment/"),
#                                 10)):
#     print (i, key)
    
#!s3cmd ls s3://aws-publicdatasets/common-crawl/parse-output/

# <codecell>

!s3cmd ls s3://aws-publicdatasets/common-crawl/parse-output/valid_segments.txt

# <codecell>

k = bucket.get_key("common-crawl/parse-output/valid_segments.txt")
s = k.get_contents_as_string()

valid_segments = filter(None, s.split("\n"))

print (len(valid_segments), valid_segments[0])

# <codecell>

# focus on s3://aws-publicdatasets/common-crawl/crawl-data/CC-MAIN-2014-15/
# http://commoncrawl.org/april-2014-crawl-data-available/


!s3cmd ls s3://aws-publicdatasets/common-crawl/crawl-data/CC-MAIN-2014-15/

# <markdowncell>

# # April 2014 crawl
# 
# 
# http://commoncrawl.org/april-2014-crawl-data-available/
# 
# *    all segments (CC-MAIN-2014-15/segment.paths.gz)
# *    all WARC files (CC-MAIN-2014-15/warc.paths.gz)
# *    all WAT files (CC-MAIN-2014-15/wat.paths.gz)
# *    all WET files (CC-MAIN-2014-15/wet.paths.gz)
# 
# https://aws-publicdatasets.s3.amazonaws.com/common-crawl/crawl-data/CC-MAIN-2014-15/segment.paths.gz

# <codecell>

list(keys_in_bucket(bucket, "common-crawl/crawl-data/CC-MAIN-2014-15/"))

# <codecell>

import gzip
import StringIO

def gzip_from_key(bucket, key_name):
    k = bucket.get_key(key_name)
    f = gzip.GzipFile(fileobj=StringIO.StringIO(k.get_contents_as_string()))
    return f

def segments_from_gzip(gz):
    s = gz.read()
    return filter(None, s.split("\n"))

# <codecell>

# let's parse segment.paths.gz

valid_segments = segments_from_gzip(gzip_from_key(bucket, 
                    "common-crawl/crawl-data/CC-MAIN-2014-15/segment.paths.gz"))
valid_segments[:5]

# <headingcell level=1>

# WAT:  metadata files

# <markdowncell>

# all WAT files (CC-MAIN-2014-15/wat.paths.gz)

# <codecell>

wat_segments = segments_from_gzip(gzip_from_key(bucket, 
                    "common-crawl/crawl-data/CC-MAIN-2014-15/wat.paths.gz"))
len(wat_segments)

# <codecell>

wat_segments[0]

# <markdowncell>

# http://commoncrawl.org/navigating-the-warc-file-format/
# 
# json file
# 
# forgot to check how big the file is before downloading it.

# <codecell>

k = bucket.get_key(wat_segments[0])
k.size

# <codecell>

def get_key_sizes(bucket, keys):
    sizes = []
    for key in keys:
        k = bucket.get_key(key)
        sizes.append((key, k.size if hasattr(k, 'size') else 0))
    return sizes

# <codecell>

get_key_sizes(bucket, wat_segments[0:20])

# <codecell>

# http://stackoverflow.com/questions/2348317/how-to-write-a-pager-for-python-iterators/2350904#2350904        
def grouper(iterable, page_size):
    page= []
    for item in iterable:
        page.append( item )
        if len(page) == page_size:
            yield page
            page= []
    if len(page) > 0:
        yield page

# <codecell>

# feed this calculation to multyvac

from itertools import islice
import multyvac

def submit_jobs_to_calc_wat_file_sizes():
    page_size = 100
    jids = []
    for page in grouper(wat_segments, page_size):
        jid = multyvac.submit(get_key_sizes, bucket, page)
        jids.append(jid)

# <codecell>

# when I did my calc on 2014.07.24, I got job ids 27 to 471
set(sorted(jids)) == set(range(27,472))

# <codecell>

def get_statuses(jids):

    jobs = [multyvac.get(jid) for jid in jids]
    statuses = [job.status for job in jobs]
    return statuses

# <codecell>

def get_results(jids):
    for jid in jids:
        job = multyvac.get(jid)
        yield job.get_result()
        

# <codecell>

def compile_results(jids):

    results = []

    for (i, page) in enumerate(islice(get_results(jids),None)):
        print (i)
        for result in page:
            results.append(result)
            
    return results
    
len(results)

# <codecell>

from pandas import Series, DataFrame
df = DataFrame(results, columns=['key', 'size'])
df.head()

# <codecell>

df['size'].describe()

# <codecell>

%pylab --no-import-all inline

# <codecell>

import pylab as P
P.hist(df['size'])

# <codecell>

# total byte size of all the wat files
print (format(sum(df['size']),",d"))

# <codecell>

# save results
import csv
with open('CC-MAIN-2014-15.wat.csv', 'wb') as csvfile:
    wat_writer = csv.writer(csvfile, delimiter=',',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
    wat_writer.writerow(['key', 'size'])
    for result in results:
        wat_writer.writerow(result)

# <codecell>

!head CC-MAIN-2014-15.wat.csv

# <codecell>

#s = g.read()

# <headingcell level=1>

# Taking apart a WAT file

# <codecell>

key = bucket.get_key(wat_segments[0])
url = key.generate_url(expires_in=0, query_auth=False)
url

# <codecell>

wat_segments[0]

# <codecell>

# looks like within any segment ID, we should expect warc, wat, wet buckets

!s3cmd ls s3://aws-publicdatasets/common-crawl/crawl-data/CC-MAIN-2014-15/segments/1397609521512.15/

# <codecell>

import boto
from itertools import islice
from boto.s3.key import Key
from gzipstream import GzipStreamFile
import warc
import json


def test_gzipstream():

  output = []
    
  # Let's use a random gzipped web archive (WARC) file from the 2014-15 Common Crawl dataset
  ## Connect to Amazon S3 using anonymous credentials
  conn = boto.connect_s3(anon=True)
  pds = conn.get_bucket('aws-publicdatasets')
  ## Start a connection to one of the WARC files
  k = Key(pds)
  k.key = 'common-crawl/crawl-data/CC-MAIN-2014-15/segments/1397609521512.15/warc/CC-MAIN-20140416005201-00000-ip-10-147-4-33.ec2.internal.warc.gz'

  # The warc library accepts file like objects, so let's use GzipStreamFile
  f = warc.WARCFile(fileobj=GzipStreamFile(k))
  for num, record in islice(enumerate(f),100):
    if record['WARC-Type'] == 'response':
      # Imagine we're interested in the URL, the length of content, and any Content-Type strings in there
      output.append((record['WARC-Target-URI'], record['Content-Length']))
      output.append( '\n'.join(x for x in record.payload.read().replace('\r', '').split('\n\n')[0].split('\n') if 'content-type:' in x.lower()))
      output.append( '=-=-' * 10)
 
  return output
        

# <codecell>

def warc_records(key_name, limit=None):
    conn = boto.connect_s3(anon=True)
    bucket = conn.get_bucket('aws-publicdatasets')
    key = bucket.get_key(key_name)

    # The warc library accepts file like objects, so let's use GzipStreamFile
    f = warc.WARCFile(fileobj=GzipStreamFile(key))
    for record in islice(f, limit):
        yield record

# <codecell>

# let's compute some stats on the headers
from collections import Counter
c=Counter()
[c.update(record.header.keys()) for record in warc_records(wat_segments[0],100)]
c

# <codecell>

# warc-type

# looks like 
# first record is 'warcinfo
# rest is 'metadata'

c=Counter()
[c.update([record['warc-type']]) for record in warc_records(wat_segments[0],100)]

c

# <codecell>

# content-type

c=Counter()
[c.update([record['content-type']]) for record in warc_records(wat_segments[0],100)]

c

# <codecell>

# what

# <codecell>

wrecords = warc_records(wat_segments[0])

# <codecell>

record = wrecords.next()

# <codecell>

# http://warc.readthedocs.org/en/latest/#working-with-warc-header

record.header.items()

# <codecell>

#payload
dir(record.payload)

# <codecell>

record.header.get('content-type')

# <codecell>

# payload


s = record.payload.read()
len(s)

# <codecell>

if record.header.get('content-type') == 'application/json':
    payload = json.loads(s)
else:
    payload = s
    
payload

# <codecell>

payload['Envelope']['WARC-Header-Metadata']['WARC-Target-URI']

# <codecell>

import urlparse
urlparse.urlparse(payload['Envelope']['WARC-Header-Metadata']['WARC-Target-URI']).netloc

# <codecell>

import urlparse

def netloc_count_for_segment(segment_id, limit=None):
    
    c = Counter()

    for record in warc_records(segment_id,limit):

        s = record.payload.read()
        if record.header.get('content-type') == 'application/json':
            payload = json.loads(s)
            url = payload['Envelope']['WARC-Header-Metadata'].get('WARC-Target-URI')
            if url:
                netloc = urlparse.urlparse(url).netloc
                c.update([netloc])
            else:
                c.update([None])

    return c


        

# <codecell>

%time netloc_count_for_segment(wat_segments[0],100000)

# <codecell>

import multyvac
jid = multyvac.submit(netloc_count_for_segment, wat_segments[0],150000,_core='c1', _name="wat_seg:0, 150000, c1; new gzipstream")
jid

# <codecell>

job = multyvac.get(jid)
job

# <codecell>

job.status

# <codecell>

job.get_result()

# <headingcell level=1>

# WARC files:  the final frontier

# <markdowncell>

# Is it possible to work with pieces of the new warc files without having to download the whole file?  
# 
# In the 2012 crawl data, there was an index built http://urlsearch.commoncrawl.org/ --> from which you can get a reference to an offset and length inside of the arc.gz file.  With S3, you don't need to then download the whole file but just a chunk....and that chunk itself is unpackable as a gzip file.  (nice feature of gzip?):
# 
# http://nbviewer.ipython.org/github/rdhyee/working-open-data/blob/postscript/notebooks/Day_21_CommonCrawl_Content.ipynb#Grabbing-pieces-of-the-.arc.gz-files
# 
# Is there a similar way of working with the 2014 crawl data?  That is, a way of reading off chunks of the warc file without grabbing entire warc files?

# <markdowncell>


