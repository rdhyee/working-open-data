# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <headingcell level=1>

# Goals

# <markdowncell>

# For us to learn:
# 
# * the basics of how to process CommonCrawl data by counting files and tallying file sizes in the CC crawl
# * how to do this processing in parallel fashion using PiCloud, Amazon AWS (specifically S3), the [`boto` library](http://boto.readthedocs.org/en/latest/) 
# 
# We start by writing a function to calculate stats on one given "valid segment" in the Common Crawl.  Then we'll learn how to calculate the stats for all valid segments and aggregate the data.

# <headingcell level=1>

# Prerequisites

# <markdowncell>

# Although strictly speaking, you can do all the work directly on PiCloud (where I'm handling the dependencies), you'll likely want to get PiCloud, boto, s3cmd set up locally.  See [Day 19 notes](http://nbviewer.ipython.org/urls/raw.github.com/rdhyee/working-open-data/master/notebooks/Day_19_CC_etc.ipynb) and [Day 16 PiCloud intro](http://nbviewer.ipython.org/urls/raw.github.com/rdhyee/working-open-data/master/notebooks/Day_16_PiCloud_intro.ipynb) for a refresher.  **One big reason for working locally is that you'll get charged for the time you are running a PiCloud notebook server** -- and when you are thinking, it's nice to not have to worry about the time (even if it is $0.05/hour for a running a c1 PiCloud instance.)
# 
# Also ask for help if you are having problems.

# <headingcell level=1>

# Moving notebooks between local storage and PiCloud

# <headingcell level=2>

# One way to copy this notebook from local machine to PiCloud -- use cloud.bucket.put

# <markdowncell>

# To see what's in your PiCloud bucket

# <codecell>

import cloud
cloud.bucket.list()

# <headingcell level=2>

# copying from local computer to PiCloud

# <codecell>

# http://docs.picloud.com/moduledoc.html#module-cloud.bucket

import os
# only if we not running on picloud....
if not os.path.exists('/home/picloud/notebook'):
    pass
    # normally I keep this line commented to prevent accidental copying if I run the notebook through.
    cloud.bucket.put('Day_20_CommonCrawl_Starter.ipynb', 'notebook/Day_20_CommonCrawl_Starter.ipynb')

# <headingcell level=2>

# copying from PiCloud to local machine

# <codecell>

import os

if not os.path.exists('/home/picloud/notebook'):
    pass
    # normally I keep this line commented to prevent accidental copying if I run the notebook through.
    # note the new local name -- to make it less likely to overwrite something I'm doing locally.
    #cloud.bucket.get('notebook/Day_20_CommonCrawl_Starter.ipynb', 'Day_20_CommonCrawl_Starter_from_picloud.ipynb')

# <markdowncell>

# **Warning:** I don't think you'll immediately see the notebook changes reflected in an already running PiCloud notebook server -- at least, that was my experience.

# <markdowncell>

# There are other ways to interact with PiCloud -- using picloud ssh-info and scp --See [SSH into a job](http://docs.picloud.com/job_mgmt_adv.html#client-adv-ssh-into-job) and some [rough notes](https://www.evernote.com/shard/s1/sh/a9fab233-1857-4f01-8437-805be0e6fe22/593a1224dd150d6cf1cea6bb9886c22d).  The following code shows how to use `picloud ssh-info JID` to get the right ssh scp commands.
# 
# You can read off the job id for your PiCloud notebook server from the upper right corner of https://www.picloud.com/accounts/notebook/:
# 
# <img src="https://www.evernote.com/shard/s1/sh/646f953b-2c86-4b52-9deb-6dbe4f6ebc9e/26894da1003bf19d26cb0033f89097b4/res/a6f9765c-fa23-4521-9b02-3660134c9b80/PiCloud_%7C_Notebook-20130404-110444.jpg.jpg?resizeSmall&width=832">
# 

# <codecell>

import re

# put the job id of your notebook server after ssh-info

NOTEBOOK_SERVER_RUNNING = False
NOTEBOOK_SERVER_JID = 501

def to_picloud(nb_name):
    scp_to_command =  "scp -q -i {identity} -P {port} {nb_name} {username}@{address}:/home/picloud/notebook/".format(nb_name=nb_name, **ssh_info_output)
    return scp_to_command

if NOTEBOOK_SERVER_RUNNING:
    ssh_info_output = !picloud ssh-info $NOTEBOOK_SERVER_JID
    ssh_info_output = dict(zip( *[filter(None, re.split("\s+", l)) for l in ssh_info_output]))
#print ssh_info_output

    ssh_command = "ssh -q -i {identity} {username}@{address} -p {port}".format(**ssh_info_output)


    print ssh_command
    print to_picloud("Day_20_CommonCrawl_Starter.ipynb")

# you can even run the scp command from within iPython notebook -- uncomment following lines
#    to_picloud = to_picloud("Day_20_CommonCrawl_Starter.ipynb")
#    ! $to_picloud

# <markdowncell>

# **Running scp to the live notebook server machine will actually update the notebooks.**

# <headingcell level=1>

# Learning about Common Crawl structure

# <markdowncell>

# Good to review Dave Lester's talk: http://www.slideshare.net/davelester/introduction-to-common-crawl  
# 
# If you need general intro to Common Crawl, watch the [Common Crawl Video](https://www.youtube.com/watch?v=ozX4GvUWDm4).

# <headingcell level=2>

# Common Crawl data stored in Amazon S3

# <markdowncell>

# The Common Crawl data structure is documented at https://commoncrawl.atlassian.net/wiki/display/CRWL/About+the+Data+Set. To quote the docs:
# 
# The entire Common Crawl data set is stored on Amazon S3 as a Public Data Set:
# 
#     http://aws.amazon.com/datasets/41740
# 
# The data set is divided into three major subsets:
# 
# * Archived Crawl #1 - s3://aws-publicdatasets/common-crawl/crawl-001/ - crawl data from 2008/2010
# * Archived Crawl #2 - s3://aws-publicdatasets/common-crawl/crawl-002/ - crawl data from 2009/2010
# * Current Crawl - s3://aws-publicdatasets/common-crawl/parse-output/ - crawl data from 2012
# 
# The two archived crawl data sets are stored in folders organized by the year, month, date, and hour the content was crawled.  For example:
# 
#     s3://aws-publicdatasets/common-crawl/crawl-002/2010/01/06/10/1262847572760_10.arc.gz
# 
# The current crawl data set is stored in the "parse-output" folder in a similar manner to how Nutch stores archives.  Crawl data is stored in a "segments" subfolder, then in a folder that starts with the UNIX timestamp of crawl start time.  For example:
# 
#     s3://aws-publicdatasets/common-crawl/parse-output/segment/1341690169105/1341826131693_45.arc.gz

# <headingcell level=2>

# Using s3cmd and boto to confirm the examples from the documentation

# <codecell>

# this key, secret access to aws-publicdatasets only -- created for WwOD 13 student usage

# turns out there is an anonymous mode in boto for public data sets:
# https://github.com/keiw/common_crawl_index/commit/ad341d0a41a828f260c9c08419dadff0dac6cf5b#L0R33
#  conn=S3Connection(anon=True) will work instead of conn= S3Connection(KEY, SECRET) -- but there seems to be 
# a bug in how S3Connection gets pickled for anon=True -- so for now, just use the KEY, SECRET

KEY = 'AKIAJH2FD7572FCTVSSQ'
SECRET = '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'

# <markdowncell>

# You can use this key/secret pair to configure both `boto` and `s3cmd`

# <codecell>

# s3cmd installed in custom PiCloud environment -- and maybe in your local environment too

# confirm s3://aws-publicdatasets/common-crawl/crawl-002/2010/01/06/10/1262847572760_10.arc.gz
# doc for s3cmd: http://s3tools.org/s3cmd

!s3cmd ls s3://aws-publicdatasets/common-crawl/crawl-002/2010/01/06/10/1262847572760_10.arc.gz

# <headingcell level=3>

# EXERCISE:  use s3cmd to confirm existence of `s3://aws-publicdatasets/common-crawl/parse-output/segment/1341690169105/1341826131693_45.arc.gz`

# <codecell>






# <headingcell level=2>

# using s3cmd to look at parse-output and valid_segments.txt in current crawl

# <codecell>

# looking at parse-output itself

!s3cmd ls s3://aws-publicdatasets/common-crawl/parse-output

# <codecell>

# looking at what is contained by parse-output "folder"

!s3cmd ls s3://aws-publicdatasets/common-crawl/parse-output/

# <markdowncell>

# There is a list of "valid segments" in 
# 
#     s3://aws-publicdatasets/common-crawl/parse-output/valid_segments.txt
# 
# -- a list of segments that are part of the current crawl.  Let's download it and study it.
# 
# See [discussion about valid segments](https://groups.google.com/forum/#!msg/common-crawl/QYTmnttZZyo/NPiXvK8ZeiMJ)

# <codecell>

!s3cmd ls s3://aws-publicdatasets/common-crawl/parse-output/valid_segments.txt

# <codecell>

# we can download it:

!s3cmd get s3://aws-publicdatasets/common-crawl/parse-output/valid_segments.txt

# <codecell>

!head valid_segments.txt

# <headingcell level=2>

# using boto to study parse-output and valid_segments.txt

# <codecell>

# http://boto.s3.amazonaws.com/s3_tut.html

import boto
from boto.s3.connection import S3Connection

from itertools import islice

conn = S3Connection(KEY,SECRET)

# turns out there is an anonymous mode in boto for public data sets:
# https://github.com/keiw/common_crawl_index/commit/ad341d0a41a828f260c9c08419dadff0dac6cf5b#L0R33
#conn=S3Connection(anon=True)

bucket = conn.get_bucket('aws-publicdatasets')
for key in islice(bucket.list(prefix="common-crawl/parse-output/", delimiter="/"),None):
    print key.name.encode('utf-8')

# <codecell>

# get valid_segments
# https://commoncrawl.atlassian.net/wiki/display/CRWL/About+the+Data+Set

import boto
from boto.s3.connection import S3Connection

conn = S3Connection(KEY, SECRET)
bucket = conn.get_bucket('aws-publicdatasets')

k = bucket.get_key("common-crawl/parse-output/valid_segments.txt")
s = k.get_contents_as_string()

valid_segments = filter(None, s.split("\n"))

print len(valid_segments), valid_segments[0]

# <codecell>

# valid_segments are Unix timestamps (in ms) -- confirm current crawl is from 2012

import datetime
datetime.datetime.fromtimestamp(float(valid_segments[0])/1000.)

# <headingcell level=1>

# Using boto to compile stats on each valid segment

# <markdowncell>

# As of the time of this writing (April 4, 2013), there are 177 valid segments in the current crawl.  Now, it's time to figure out how to write a Python function called `segment_stats` that takes a segment id and an optional `stop` parameter (for the max number of keys to iterate through) of the form
# 
#     def segment_stats(seg_id, stop=None):
#         pass
#         # YOUR EXERCISE TO FILL IN
# 
# and returns a `dict` with 2 keys:  
# 
# * `count` holding the number of keys inside the given valid segment
# * `size` holding the total number of bytes held in the keys
# 
# broken down by file type (there are 3 major types):
# 
# * `arg.gz` for the 
# * 'metadata' for the metadata files
# * 'textData' for the textdata files
# * 'success' for success files
# 
# For example:
# 
#     segment_stats('1346823845675', None)
# 
# should return:
# 
#     {
#      'count': {'arc.gz': 11904, 'metadata': 4377, 'success': 1, 'textData': 4377},
#      'size': {'arc.gz': 967409519222,
#           'metadata': 187079951008,
#           'success': 0,
#           'textData': 129994977292}
#     }

# <headingcell level=2>

# Start by looking at a small subset of keys from valid_segments[0]

# <markdowncell>

# Since it can take 10-50 seconds or so to retrieve all the keys in a valid segment, it's worth limiting to say first 10 to get a feel for what you can do with a key.  Run the following:

# <codecell>

from itertools import islice

import boto
from boto.s3.connection import S3Connection

conn = S3Connection(KEY, SECRET)
bucket = conn.get_bucket('aws-publicdatasets')
for key in islice(bucket.list(prefix="common-crawl/parse-output/segment/1346823845675/", delimiter="/"),10):
    print key.name.encode('utf-8')

# <codecell>

# WARNING -- this might take a bit of time to run -- run it to see how long it takes you to get all the keys in this
# segment.  time depends on where you are running this code

%time all_files = list(islice(bucket.list(prefix="common-crawl/parse-output/segment/1346823845675/", delimiter="/"),None))
print len(all_files), all_files[0]

# <markdowncell>

# But it's useful now to have `all_files` to hold all the keys under the segment `1346823845675`  Note, for example, you can get the size of the file and the name -- and the type of file (boto.s3.key.Key)

# <codecell>

# http://boto.readthedocs.org/en/latest/ref/s3.html#module-boto.s3.key

file0 = all_files[0]
type(file0), file0.name, file0.size

# <codecell>

import boto
from boto.s3.connection import S3Connection

# this key, secret access to aws-publicdatasets only -- createdd for WwOD 13 student usage
KEY = 'AKIAJH2FD7572FCTVSSQ'
SECRET = '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'

from itertools import islice
from pandas import DataFrame

conn= S3Connection(KEY, SECRET)
bucket = conn.get_bucket('aws-publicdatasets')

# you might find this conversion function between DataFrame and a list of a regular dict useful
#https://gist.github.com/mikedewar/1486027#comment-804797
def df_to_dictlist(df):
    return [{k:df.values[i][v] for v,k in enumerate(df.columns)} for i in range(len(df))]

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
        return 'other'
    
def segment_stats(seg_id, stop=None):
    
    # FILL IN WITH YOUR CODE
    
    return {
      'count': {'arc.gz': 11904, 'metadata': 4377, 'success': 1, 'textData': 4377},
      'size': {'arc.gz': 967409519222,
      'metadata': 187079951008,
      'success': 0,
      'textData': 129994977292}
     }
    

