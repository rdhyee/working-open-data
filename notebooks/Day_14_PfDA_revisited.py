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

# <codecell>

# Naive scatter plot

scatter(frame[frame.ll.notnull()]['ll'].apply(lambda x: x[1]), frame[frame.ll.notnull()]['ll'].apply(lambda x: x[0]), 3, color="g" )

# <codecell>

from itertools import izip

dots = izip(frame[frame.ll.notnull()]['ll'].apply(lambda x: x[1]).values,
            frame[frame.ll.notnull()]['ll'].apply(lambda x: x[0]))

# <codecell>

# http://matplotlib.org/basemap/users/mapcoords.html

from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import numpy as np

# setup Lambert Conformal basemap.
m = Basemap(projection='merc',llcrnrlat=-80,urcrnrlat=80,\
            llcrnrlon=-180,urcrnrlon=180,lat_ts=20,resolution='c')

# draw a boundary around the map, fill the background.
# this background will end up being the ocean color, since
# the continents will be drawn on top.
m.drawmapboundary(fill_color='aqua')
# fill continents, set lake color same as ocean color.
m.fillcontinents(color='coral',lake_color='aqua')

# draw state boundaries too
# http://matplotlib.org/basemap/api/basemap_api.html#mpl_toolkits.basemap.Basemap.drawstates
m.drawstates(linewidth=0.1)


m.drawparallels(np.arange(-90.,91.,30.))
m.drawmeridians(np.arange(-180.,181.,60.))


# plot blue dot on Boulder, colorado and label it as such.
lon, lat = -104.237, 40.125 # Location of Boulder
# convert to map projection coords.
# Note that lon,lat can be scalars, lists or numpy arrays.
xpt,ypt = m(lon,lat)
# convert back to lat/lon
lonpt, latpt = m(xpt,ypt,inverse=True)
m.plot(xpt,ypt,'bo',markersize=5)  # plot a blue dot there

from itertools import izip

dots = izip(frame[frame.ll.notnull()]['ll'].apply(lambda x: x[1]).values,
            frame[frame.ll.notnull()]['ll'].apply(lambda x: x[0]))

for dot in dots:
    (xpt, ypt) = m(dot[0], dot[1])
    m.plot(xpt, ypt, 'bo', markersize=2)
    

# <codecell>

# http://matplotlib.org/basemap/users/mapcoords.html

from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import numpy as np

# setup Lambert Conformal basemap.
m = Basemap(projection='merc',llcrnrlat=-80,urcrnrlat=80,\
            llcrnrlon=-180,urcrnrlon=180,lat_ts=20,resolution='c')

# draw a boundary around the map, fill the background.
# this background will end up being the ocean color, since
# the continents will be drawn on top.
m.drawmapboundary(fill_color='aqua')
# fill continents, set lake color same as ocean color.
m.fillcontinents(color='coral',lake_color='aqua')

# draw state boundaries too
# http://matplotlib.org/basemap/api/basemap_api.html#mpl_toolkits.basemap.Basemap.drawstates
m.drawstates(linewidth=0.1)


m.drawparallels(np.arange(-90.,91.,30.))
m.drawmeridians(np.arange(-180.,181.,60.))


# plot blue dot on Boulder, colorado and label it as such.
lon, lat = -104.237, 40.125 # Location of Boulder
# convert to map projection coords.
# Note that lon,lat can be scalars, lists or numpy arrays.
xpt,ypt = m(lon,lat)
# convert back to lat/lon
lonpt, latpt = m(xpt,ypt,inverse=True)
m.plot(xpt,ypt,'bo',markersize=5)  # plot a blue dot there


(xpt, ypt) = m(frame[frame.ll.notnull()]['ll'].apply(lambda x: x[1]), 
               frame[frame.ll.notnull()]['ll'].apply(lambda x: x[0]))
m.plot(xpt, ypt, 'bo', markersize=2)
    

# the following doesn't work for some reason....
#m.scatter(frame[frame.ll.notnull()]['ll'].apply(lambda x: x[1]), frame[frame.ll.notnull()]['ll'].apply(lambda x: x[0]), 3, color="g" )
# put some text next to the dot, offset a little bit
# (the offset is in map projection coordinates)

# <markdowncell>

# timestamp -- range -- when exactly?  
# 
# histogram?

# <codecell>

frame.t.describe()

# <codecell>

frame.t.dropna().apply(datetime.datetime.fromtimestamp)

# <headingcell level=2>

# Exercise:  confirm the value of the earliest and latest of the timestamps -- compute earliest_dt, latest_dt

# <codecell>

# FILL IN 

earliest_dt = datetime.datetime.fromtimestamp(frame.t.min())
assert earliest_dt == datetime.datetime(2012, 3, 16, 11, 40, 47)

latest_dt = datetime.datetime.fromtimestamp(frame.t.max())
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

#http://docs.python.org/2/library/urlparse.html
from urlparse import urlparse

s  = frame.u.dropna().apply(lambda u: urlparse(u)[1])
netlocs = s.groupby(s).size().order()[::-1]

# https://github.com/pydata/pandas/issues/240
assert isinstance(netlocs, Series)
assert set(list(netlocs[:5].iteritems())) == set([(u'www.whitehouse.gov', 169),
     (u'www.monroecounty.gov', 121),
     (u'www.fda.gov', 112),
     (u'www.nasa.gov', 733),
     (u'www.nysdot.gov', 836)])

# <headingcell level=1>

# movielens dataset

# <markdowncell>

# PDA p. 26 
# 
# http://www.grouplens.org/node/73 --> there's also a 10 million ratings dataset -- would be interesting to try out to test scalability
# of running IPython notebook on laptop
# 

# <codecell>

# let's take a look at the data

# my local dir: /Users/raymondyee/D/Document/Working_with_Open_Data/pydata-book/ch02/movielens

!head $MOVIELENS_DIR/movies.dat

# <codecell>

# how many movies?
!wc $MOVIELENS_DIR/movies.dat

# <codecell>

!head $MOVIELENS_DIR/users.dat

# <codecell>

!head $MOVIELENS_DIR/ratings.dat

# <codecell>

import pandas as pd
import os

unames = ['user_id', 'gender', 'age', 'occupation', 'zip']
users = pd.read_table(os.path.join(MOVIELENS_DIR, 'users.dat'), sep='::', header=None,
  names=unames)

rnames = ['user_id', 'movie_id', 'rating', 'timestamp']
ratings = pd.read_table(os.path.join(MOVIELENS_DIR, 'ratings.dat'), sep='::', header=None,
  names=rnames)

mnames = ['movie_id', 'title', 'genres']
movies = pd.read_table(os.path.join(MOVIELENS_DIR, 'movies.dat'), sep='::', header=None,
  names=mnames, encoding='iso-8859-1')

# <codecell>

movies[:100]

# <codecell>

import traceback

try:
    movies[:100]
except:
    traceback.print_exc()

# <codecell>

# explicit encoding of movies file

import pandas as pd
import codecs


unames = ['user_id', 'gender', 'age', 'occupation', 'zip']
users = pd.read_table(os.path.join(MOVIELENS_DIR, 'users.dat'), sep='::', header=None,
  names=unames)

rnames = ['user_id', 'movie_id', 'rating', 'timestamp']
ratings = pd.read_table(os.path.join(MOVIELENS_DIR, 'ratings.dat'), sep='::', header=None,
  names=rnames)


movies_file = codecs.open(os.path.join(MOVIELENS_DIR, 'movies.dat'), encoding='iso-8859-1')

mnames = ['movie_id', 'title', 'genres']
movies = pd.read_table(movies_file, sep='::', header=None,
  names=mnames)


# <codecell>

movies[:100]

# <codecell>

users[:5]

# <codecell>

movies[:100]

# <markdowncell>

# hmmm...age 1?  Where to learn about occupation types?  We have zip data...so it'd be fun to map.  Might be useful to look at
# distribution of age, gender, and zip.

# <codecell>

# confirm type of users as DataFram and list number of users

type(users), len(users)

# <codecell>

users.index, users.columns

# <codecell>

# row 0

users.ix[0]

# <codecell>

# a specific "cell" of users

users.ix[0]['occupation']

# <codecell>

# how to get stats for a column?

users['gender'].describe()

# <codecell>

from collections import Counter

Counter(users['gender'])

# <codecell>

users['age'].describe()

# <codecell>

users['age'].hist()

# <codecell>

ratings['rating'].hist()

# <codecell>

ratings['timestamp'].hist()

# <markdowncell>

# how to convert to datetime.datetime and plot hist in those units?  **come back to this task**
# 
# * convert units to datetime
# * plot timeseries

# <codecell>


import datetime
datetime.datetime.fromtimestamp(ratings['timestamp'][0])

# <codecell>

ratings['timestamp'].order().apply(datetime.datetime.fromtimestamp) #apply(datetime.datetime.fromtimestamp)

# <headingcell level=2>

# merge datasets

# <codecell>

data = pd.merge(pd.merge(ratings,users), movies)

# <codecell>

data

# <codecell>

data[:5]

# <markdowncell>

# http://www.grouplens.org/system/files/ml-1m-README.txt has the key for occupations and age ranges:
# 
# *  0:  "other" or not specified
# *  1:  "academic/educator"
# *  2:  "artist"
# *  3:  "clerical/admin"
# *  4:  "college/grad student"
# *  5:  "customer service"
# *  6:  "doctor/health care"
# *  7:  "executive/managerial"
# *  8:  "farmer"
# *  9:  "homemaker"
# * 10:  "K-12 student"
# * 11:  "lawyer"
# * 12:  "programmer"
# * 13:  "retired"
# * 14:  "sales/marketing"
# * 15:  "scientist"
# * 16:  "self-employed"
# * 17:  "technician/engineer"
# * 18:  "tradesman/craftsman"
# * 19:  "unemployed"
# * 20:  "writer"

# <codecell>

from collections import Counter
Counter(data['occupation'])

# <codecell>

data.occupation.groupby(data.occupation).size()

# <codecell>

mean_ratings = data.pivot_table('rating', rows='title', cols='gender', aggfunc='mean')

# <codecell>

mean_ratings

# <codecell>

mean_ratings[:5]

# <codecell>

# trying to pull together both male and female -- works

data.pivot_table(values='rating', rows='title')

# <codecell>

data.groupby('title').size()

# <headingcell level=2>

# check on encoding of the movie files

# <codecell>

import codecs
from itertools import islice

fname = os.path.join(MOVIELENS_DIR, "movies.dat")

f = codecs.open(fname, encoding='iso-8859-1')
for line in islice(f,100):
    print line

# <codecell>

import pandas as pd
import codecs

movies_file = codecs.open(os.path.join(MOVIELENS_DIR, 'movies.dat'), encoding='iso-8859-1')

mnames = ['movie_id', 'title', 'genres']
movies = pd.read_table(movies_file, sep='::', header=None,
  names=mnames)

print (movies.ix[72]['title'] == u'Misérables, Les (1995)')

# <headingcell level=2>

# collapse to 250 most frequently rated movies (p. 29)  

# <codecell>

ratings_by_title = data.groupby('title').size()

# <codecell>

ratings_by_title.order(ascending=False).plot()

# <codecell>

ratings_by_title >= 250

# <codecell>

active_titles = ratings_by_title.index[ratings_by_title >= 250]

# <codecell>

active_titles

# <codecell>

len(active_titles)

# <codecell>

# now subset

mean_ratings = mean_ratings.ix[active_titles]

# <codecell>

mean_ratings

# <codecell>

# top films among female viewers

mean_ratings.sort_index(by='F', ascending=False)[:10]

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

# which names that are in both sexes?  
# let me do it with Python sets

names1880[names1880.sex == 'M'], names1880[names1880.sex == 'F']

# <codecell>

m_names = set(names1880[names1880.sex == 'M']['name'])
f_names = set(names1880[names1880.sex == 'F']['name'])

len(m_names & f_names)

# <codecell>

# almost...

try:
    k = names1880.groupby('name').ix(names1880.groupby('name').size() == 2)
except Exception as e:
    print e
else:
    print k

# <codecell>



count_sex = names1880.groupby('name').size()
mf_names = count_sex.index[count_sex == 2]

names1880.ix[mf_names]

# <codecell>

from itertools import islice

mf_names =(k for (k, g) in names1880.groupby('name') if len(g) == 2)

list(islice(mf_names, 5))

# <codecell>

names1880.groupby('name')

# <codecell>

names1880.groupby('name').size().values

# <headingcell level=2>

# loading all data into Pandas -- how well does this work?

# <codecell>

!ls $NAMES_DIR

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

# how to calculate the total births / year

names.groupby('year').sum().plot(title="total births by year")

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

# proportion for Raymond
names.name

# <codecell>

# max / min totals and when? -- awkward -- must be a better way
total_births_sum = names.groupby('year').sum()
max_value = list(total_births_sum.max())[0]
min_value = list(total_births_sum.min())[0]

is_max = total_births_sum.births == max_value
is_min = total_births_sum.births == min_value
is_max[is_max], is_min[is_min]

# <codecell>

total_births_sum.diff().plot()

# <codecell>

total_births.sum().sum()

# <codecell>

names[(names.name=='Raymond') & (names.sex=='M')][['year', 'births']].set_index(keys='year').plot(title="Raymond")

# <codecell>

# plot multiple names on same plot or as multiple axes

# <codecell>

def name_sex_count_in_year(name,sex):
    return names[(names.name==name) & (names.sex==sex)][['year', 'births']].set_index(keys='year')

def name_sex_prop_in_year(name,sex):
    return names[(names.name==name) & (names.sex==sex)][['year', 'prop']].set_index(keys='year')

name_df = DataFrame(index=arange(1880,2010))

name_df['Raymond'] = name_sex_count_in_year('Raymond','M')
name_df['Laura'] = name_sex_count_in_year('Laura','F')

name_df.plot()

# <codecell>

name_df = DataFrame(index=arange(1880,2010))

name_df['Raymond'] = name_sex_prop_in_year('Raymond','M')
name_df['Laura'] = name_sex_prop_in_year('Laura','F')

name_df.plot()

# <codecell>

total_births[:5]

# <codecell>

total_births.plot(title='Total births by sex and year')

# <codecell>

# http://en.wikipedia.org/wiki/Human_sex_ratio
# make an agg figure
fig = figure()

# meaning of 111: http://stackoverflow.com/a/3584933/7782
ax = fig.add_subplot(111)
ax.set_title('Ratio of M to F births')

cum_ratio_by_sex = total_births.M.cumsum() / total_births.F.cumsum()
cum_ratio_by_sex.plot(ax=ax, label="cumulative", color="red")

# add instantaneous ratio

annual_ratio_by_sex = total_births.M / total_births.F
annual_ratio_by_sex.plot(ax=ax, label="annual", color="green")

ax.legend(loc='best')

fig.canvas.draw()

# <codecell>

# number of names over time
names.groupby('year').count()[['name']].plot()

# <codecell>

def get_top1000(group):
    return group.sort_index(by='births', ascending=False)[:1000]
grouped = names.groupby(['year', 'sex'])
top1000 = grouped.apply(get_top1000)

# <codecell>

fig = figure()

# meaning of 111: http://stackoverflow.com/a/3584933/7782
ax = fig.add_subplot(111)
ax.set_title('Entropy of names')

S_male = names[names.sex=='M'].groupby('year').prop.agg(lambda x: sum([-j*log(j) for j in x])) # apply(lambda x: -x*log(x))
S_male.plot(ax=ax, label="M", color="blue")

S_female = names[names.sex=='F'].groupby('year').prop.agg(lambda x: sum([-j*log(j) for j in x])) # apply(lambda x: -x*log(x))
S_female.plot(ax=ax, label="F", color="red")

ax.legend(loc='best')
ax.set_ylim(0)

fig.canvas.draw()

# <headingcell level=2>

# Names that are both M and F

# <codecell>

names[names.sex=='M'].groupby('name').sum().births.order()[::-1]

# <codecell>

male_names = names[names.sex=='M'].groupby('name').sum().index
female_names = names[names.sex=='F'].groupby('name').sum().index


# <headingcell level=3>

# number of unique names in data set

# <codecell>

len(male_names + female_names)

# <codecell>

len(np.unique(names.name.values))

# <codecell>

# average length of names in general 

names.name.str.len().mean()

# <codecell>

# average length of name by year

names['name_len'] = names.name.str.len()
names.groupby('year').name_len.mean().plot()
del names['name_len']

# <codecell>

fig = figure()

# meaning of 111: http://stackoverflow.com/a/3584933/7782
ax = fig.add_subplot(111)
ax.set_title('average length of name')

names['name_len'] = names.name.str.len()

names[names.sex=='M'].groupby('year').name_len.mean().plot(ax=ax, label="M", color="blue")
names[names.sex=='F'].groupby('year').name_len.mean().plot(ax=ax, label="F", color="red")

#del names['name_len']

ax.legend(loc='best')


fig.canvas.draw()

# <codecell>

# calculate number of M, F, M/F names in aggregate and then over time

names[names.year==2010].groupby(['name', 'year']).sex.count().value_counts()

