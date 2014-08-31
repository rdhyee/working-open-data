import sys
import json
from hadoop.io import SequenceFile
from itertools import islice, izip

from collections import Counter

import datetime

import boto
from boto.s3.connection import S3Connection

import cloud

# this key, secret access to aws-publicdatasets only -- created for WwOD 13 student usage

# turns out there is an anonymous mode in boto for public data sets:
# https://github.com/keiw/common_crawl_index/commit/ad341d0a41a828f260c9c08419dadff0dac6cf5b#L0R33
#  conn=S3Connection(anon=True) will work instead of conn= S3Connection(KEY, SECRET) -- but there seems to be 
# a bug in how S3Connection gets pickled for anon=True -- so for now, just use the KEY, SECRET


conn = S3Connection()
bucket = conn.get_bucket('aws-publicdatasets')

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


def valid_segments():
    # get valid_segments
    # https://commoncrawl.atlassian.net/wiki/display/CRWL/About+the+Data+Set
            
    k = bucket.get_key("common-crawl/parse-output/valid_segments.txt")
    s = k.get_contents_as_string()
    
    valid_segments = filter(None, s.split("\n"))
    return valid_segments

# you might find this conversion function between DataFrame and a list of a regular dict useful
# https://gist.github.com/mikedewar/1486027#comment-804797

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

    from pandas import DataFrame

    all_files = islice(bucket.list(prefix="common-crawl/parse-output/segment/{0}/".format(seg_id), delimiter="/"),stop)
    df = DataFrame([{'size': f.size if hasattr(f, 'size') else 0, 'name':f.name, 'type':cc_file_type(f.name)} for f in all_files])
    return {'count': df_to_dictlist(df[['size','type']].groupby('type').count()[['size']].T)[0],
            'size': df_to_dictlist(df[['size', 'type']].groupby('type').sum().astype('int64').T)[0]}
   

# another version of segment_stats that doesn't use DataFrame

def segment_stats2(seg_id, stop=None):
    from collections import Counter
    file_count = Counter()
    byte_count = Counter()
    
    all_files = islice(bucket.list(prefix="common-crawl/parse-output/segment/{0}/".format(seg_id), delimiter="/"),stop)
    for f in all_files:
        file_type = cc_file_type(f.name)
        file_count.update({file_type: 1})
        byte_count.update({file_type: f.size if hasattr(f, 'size') else 0})
    
    return {'count': dict(file_count),
            'size': dict(byte_count)}

def run_jobs(valid_segments, n_tasks=None, local=True, f=segment_stats2, env='/rdhyee/Working_with_Open_Data'):
    
    # http://docs.picloud.com/cloud_cloudmp.html 
    
    if local:
        CLOUD = cloud.mp
    else:
        CLOUD = cloud

    jids = CLOUD.map(f, valid_segments[:n_tasks], _env=env)
    return jids

def print_iresults(jids, local=True):
       
    if local:
        CLOUD = cloud.mp
    else:
        CLOUD = cloud
        
    file_counter = Counter()
    byte_counter = Counter()

    problems = []

    for (i, result) in enumerate(CLOUD.iresult(jids)):
        try:
            file_counter.update(result['count'])
            byte_counter.update(result['size'])
            print i, byte_counter['arc.gz']
        except Exception as e:
            print i, e
            problems.append((seg_id, e))
        

def tally_results(jids, local=True):
    """tabulates results for jids"""
    
    from pandas import DataFrame

    if local:
        CLOUD = cloud.mp
    else:
        CLOUD = cloud    

    jobs_info = CLOUD.info(jids,
                 info_requested=['created', 'finished', 'runtime', 'cputime']
                 )

    jobs_counter= Counter()
    [jobs_counter.update(dict([(k, v[k]) for k in ('cputime.system', 'cputime.user', 'runtime')])) for v in jobs_info.values()]

    file_counter = Counter()
    byte_counter = Counter()

    problems = []

    for (i, result) in enumerate(CLOUD.iresult(jids)):
        try:
            file_counter.update(result['count'])
            byte_counter.update(result['size'])
        except Exception as e:
            print i, e
            problems.append((seg_id, e))
            
    # generate something to plot
    started = [{'jid':k, 'time':v['finished'] - datetime.timedelta(seconds=v['runtime']), 'count': 1} for (k,v) in jobs_info.items()]
    finished = [{'jid':k, 'time':v['finished'], 'count': -1} for (k,v) in jobs_info.items()]

    df = DataFrame(started + finished)

    return ({
            'runtime': jobs_counter['runtime'],
            'cost': (jobs_counter['runtime'])/3600. * 0.05,
            'count': dict(file_counter),
            'size': dict(byte_counter),
            'problems':problems,
            'cores_vs_time_x': df.sort_index(by='time')['time'],
            'cores_vs_time_y': df.sort_index(by='time')['count'].cumsum()
            })
 