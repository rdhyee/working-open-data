# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <markdowncell>

# **Chapter 2, 3 of PDA**

# <codecell>

import matplotlib.pyplot as plt
import numpy as np

from pylab import figure, show

from pandas import DataFrame, Series
import pandas as pd

# <headingcell level=1>

# Preliminaries: Assumed location of pydata-book files

# <markdowncell>

# To make it more practical for me to look at your homework, I'm again going to assume a relative placement of files.  I placed the files from 
# 
# https://github.com/pydata/pydata-book
# 
# in a local directory, which in my case is "/Users/raymondyee/D/Document/Working_with_Open_Data/pydata-book/" 
# 
# and then symbolically linked (`ln -s`) to the the pydata-book from the root directory of the working-open-data folder.  i.e., on OS X
# 
#     cd /Users/raymondyee/D/Document/Working_with_Open_Data/working-open-data
#     ln -s /Users/raymondyee/D/Document/Working_with_Open_Data/pydata-book/ pydata-book
# 
# That way the files from the pydata-book repository look like they sit in the working-open-data directory -- without having to actually copy the files.
# 
# With this arrangment, I should then be able to drop your notebook into my own notebooks directory and run them without having to mess around with paths.

# <codecell>

import os

USAGOV_BITLY_PATH = os.path.join(os.pardir, "pydata-book", "ch02", "usagov_bitly_data2012-03-16-1331923249.txt")
MOVIELENS_DIR = os.path.join(os.pardir, "pydata-book", "ch02", "movielens")
NAMES_DIR = os.path.join(os.pardir, "pydata-book", "ch02", "names")

assert os.path.exists(USAGOV_BITLY_PATH)
assert os.path.exists(MOVIELENS_DIR)
assert os.path.exists(NAMES_DIR)

# <markdowncell>

# **Please make sure the above assertions work**

# <headingcell level=1>

# usa.gov bit.ly example

# <markdowncell>

# (`PfDA`, p. 18)
# 
# *What's in the data file?*
# 
# <http://my.safaribooksonline.com/book/programming/python/9781449323592/2dot-introductory-examples/id2802197> :
#     
# > In 2011, URL shortening service bit.ly partnered with the United States government website usa.gov to provide a feed of anonymous data gathered from users who shorten links ending with .gov or .mil.
#     
# Hourly archive of data: <http://bitly.measuredvoice.com/bitly_archive/?C=M;O=D>

# <codecell>

open(USAGOV_BITLY_PATH).readline()

# <codecell>

import json
records = [json.loads(line) for line in open(USAGOV_BITLY_PATH)]  # list comprehension

# <headingcell level=2>

# Counting Time Zones with pandas

# <markdowncell>

# Recall what `records` is

# <codecell>

len(records)

# <codecell>

# list of dict -> DataFrame

frame = DataFrame(records)

# <codecell>

frame

# <codecell>

tz_counts = frame['tz'].value_counts()

# <codecell>

tz_counts[:10]

# <codecell>

# fillna

clean_tz = frame['tz'].fillna('Missing')
tz_counts = clean_tz.value_counts()

print tz_counts[:10]

# <codecell>

(clean_tz == '').value_counts()

# <codecell>

# '' -> 'Unknown'

clean_tz[clean_tz == ''] = 'Unknown'

# <codecell>

tz_counts = clean_tz.value_counts()

# <codecell>

tz_counts[:10]

# <codecell>

frame['a'][1]
frame['a'][50]
frame['a'][51]

# <codecell>

tz_counts[:10].plot(kind='barh', rot=0)

# <codecell>

results = Series([x.split()[0] for x in frame.a.dropna()])

# <codecell>

results[:5]

# <codecell>

results.value_counts()[:8]

# <codecell>

frame.a.notnull()

# <codecell>

frame[frame.a.notnull()]

# <codecell>

cframe = frame[frame.a.notnull()]

# <headingcell level=2>

# Let's look at the lat/long in the data

# <markdowncell>

# meaning of other attributes?
# 
# 
# http://www.usa.gov/About/developer-resources/1usagov.shtml#data
# 
# 
# 

# <codecell>

frame.ll.notnull()

# <headingcell level=2>

# EXERCISE: plot the points represented in frame.ll on a Mercator projected map

# <markdowncell>

# Hints:
# 
# * create a naive scatter plot first
# * might want to use `apply` on `Series`
# * look at the Mercator example for Boulder, CA (in Day_14_basemap_redux) -- do the mapping by a loop and then vectorize the operation

# <headingcell level=2>

# Exercise:  confirm the value of the earliest and latest of the timestamps -- compute earliest_dt, latest_dt

# <codecell>

frame.t.dropna().apply(datetime.datetime.fromtimestamp)

# <codecell>

# FILL IN 


assert earliest_dt == datetime.datetime(2012, 3, 16, 11, 40, 47)
assert latest_dt == datetime.datetime(2012, 3, 16, 12, 40, 49)

# <headingcell level=2>

# Exercise: calculate how often a given net location appears in frame.u
# 

# <markdowncell>

# Hints:
# 
# * compute `netlocs` as a Series, indexed by Network location part (<http://docs.python.org/2/library/urlparse.html>) of `frame.u`, and holding the number of times that netloc occurs in `frame.u`
# * for full marks, you must use a numpy based approach not a classic Python looping approach

# <codecell>

frame.u

# <codecell>

# FILL IN






# https://github.com/pydata/pandas/issues/240
assert isinstance(netlocs, Series)
assert set(list(netlocs[:5].iteritems())) == set([(u'www.whitehouse.gov', 169),
     (u'www.monroecounty.gov', 121),
     (u'www.fda.gov', 112),
     (u'www.nasa.gov', 733),
     (u'www.nysdot.gov', 836)])

# <headingcell level=1>

# Baby names dataset

# <codecell>

import pandas as pd
import codecs

names1880_file = codecs.open(os.path.join(NAMES_DIR,'yob2010.txt'), encoding='iso-8859-1')
names1880 = pd.read_csv(names1880_file, names=['name', 'sex', 'births'])

names1880

# <codecell>

# sort by name

names1880.sort('births', ascending=False)[:10]

# <codecell>

names1880[names1880.sex == 'F'].sort('births', ascending=False)[:10]

# <codecell>

names1880['births'].plot()

# <codecell>

names1880['births'].order(ascending=False).plot()

# <codecell>

names1880['births'].order(ascending=False).cumsum().plot()

# <codecell>

names1880['births'].count()

# <headingcell level=1>

# baby db:  straight through working out

# <codecell>

names1880.groupby('sex').births.sum()

# <codecell>

# 2010 is the last available year right now
import os

years = range(1880, 2011)

pieces = []
columns = ['name', 'sex', 'births']

for year in years:
    path = os.path.join(NAMES_DIR, 'yob%d.txt' % year)
    frame = pd.read_csv(path, names=columns)

    frame['year'] = year
    pieces.append(frame)

# Concatenate everything into a single DataFrame
names = pd.concat(pieces, ignore_index=True)

# <codecell>

names

# <codecell>

total_births = names.pivot_table('births', rows='year', cols='sex', aggfunc=sum)

# <codecell>

total_births[:5]

# <codecell>

# how to calculate the total births / year?

# <codecell>

# add prop

def add_prop(group):
    # Integer division floors
    births = group.births.astype(float)

    group['prop'] = births / births.sum()
    return group

names = names.groupby(['year', 'sex']).apply(add_prop)

# <codecell>

# verify prop
np.allclose(names.groupby(['year', 'sex']).prop.sum(), 1)

# <codecell>

total_births.plot(title='Total births by sex and year')

# <codecell>


