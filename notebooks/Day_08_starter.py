# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <headingcell level=1>

# Goals

# <markdowncell>

# To accomplish in this problem set
# 
# * more elegant operations with Pandas
# * get a start at plotting with matplotlib
# * learning how to use groupby to compare aggregates with stated totals

# <headingcell level=1>

# Preliminaries

# <markdowncell>

# Do pandas imports and set up variables for accessing census data sets

# <codecell>

import pandas as pd
from pandas import Series, DataFrame

# <codecell>

import os

DATA_DIR = os.path.join(os.pardir, "data")

# <codecell>

# see what's in the directory using os.walk

list(os.walk(os.path.join(DATA_DIR, "census")))

# <codecell>

# do shell command for linux/mac -- sorry windows users

!ls $DATA_DIR/census/*

# <headingcell level=1>

# More elegant manipulation of census DataFrame

# <headingcell level=2>

# Confirm again the assumed relative placement of files

# <codecell>

import os

# relative to parent dir
DATA_FILES = {"datadict":"data/census/DataDict.txt",
               "dataset":"data/census/DataSet.txt",
               "fips": "data/census/FIPS_CountyName.txt"}

def file_path(key):
    return os.path.join(os.pardir, DATA_FILES[key])

for file_key in DATA_FILES.keys():
    abs_fname = file_path(file_key)
    assert os.path.exists(abs_fname) is True

# <headingcell level=2>

# Construct fips_df

# <codecell>

import codecs
from itertools import islice

from pandas import Series, DataFrame

f = codecs.open(file_path("fips"), encoding='iso-8859-1')

fips_list = list()

for row in islice(f, None):
    fips_list.append({'fips': row[:5], 'geog_entity': row[6:-1]})
    
fips_df = DataFrame(fips_list)

# print out first 5 rows
fips_df[:5]

# <headingcell level=2>

# EXERCISE: add to fips_df a fips_prefix column, which is the first 2 digits in fips

# <markdowncell>

# e.g., 06 fo California

# <codecell>

# FILL IN YOUR CODE




# <codecell>

# TEST

assert np.all(fips_df[fips_df.fips == '00000']['fips_prefix'] == '00')
assert np.all(fips_df[fips_df.fips == '06000']['fips_prefix'] == '06')
assert np.all(fips_df[fips_df.fips == '06001']['fips_prefix'] == '06')

# <headingcell level=2>

# EXERCISE: add to fips_df a geog_type column ('country', 'state', or 'county')

# <markdowncell>

# ### Hints
# 
# Consider using [np.where](http://docs.scipy.org/doc/numpy/reference/generated/numpy.where.html)
# 
# and look at *PfDA*, pp. 98-100
# 
# How to take
# 
# > `np.where(fips_df.fips.str[-3:] != '000', 'county', 'is_not_county')`
# 
# and add one more np.where to differentiate between US and states?

# <codecell>

# FILL IN YOUR CODE



# <codecell>

# TEST

# check specific values

assert fips_df[fips_df.fips == '00000']['geog_type'] == 'country'
assert fips_df[fips_df.fips == '06000']['geog_type'] == 'state'
assert fips_df[fips_df.fips == '06001']['geog_type'] == 'county'


# check the numbers of various geog_type

assert set(fips_df.geog_type.value_counts().iteritems()) == set([('state', 51), ('country', 1), ('county', 3143)])

# <headingcell level=2>

# Let's load the dataset and construct df -- should be familiar stuff by now

# <codecell>

# let's try pd.read_csv 
# how to give hints about data type to pd.read_csv?

import codecs

# let's try object for fips and int for POP010210
dtype = {'fips':'S5', 'POP010210':np.int}

f = codecs.open(file_path("dataset"), encoding='iso-8859-1')
dataset_df = pd.read_csv(f, dtype=dtype)
df = pd.merge(fips_df, dataset_df)

# <codecell>

df[['fips', 'geog_entity', 'geog_type', 'POP010210']][:5]

# <headingcell level=1>

# Working with state populations

# <headingcell level=2>

# EXERCISE:  calculate a DataFrame called top_five_states_by_pop w/ 5 most populous states

# <markdowncell>

# Requirement for `top_five_states_by_pop` DataFrame:
# 
# * has only 5 rows
# * has two columns:  `geog_entity`, `POP010210`
# 
# Hints:
# 
# * you might want to make use of [`sort_index`](http://pandas.pydata.org/pandas-docs/dev/generated/pandas.DataFrame.sort_index.html)

# <codecell>

# FILL IN YOUR CODE for top_five_states_by_pop




# <codecell>

# TEST
# 5 rows, column values, and specific values

assert len(top_five_states_by_pop) == 5
assert set(top_five_states_by_pop.columns) == set(['POP010210', 'geog_entity'])
assert list(top_five_states_by_pop[['geog_entity', 'POP010210']].values.flatten()) == [u'CALIFORNIA',
 37253956L,
 u'TEXAS',
 25145561L,
 u'NEW YORK',
 19378102L,
 u'FLORIDA',
 18801310L,
 u'ILLINOIS',
 12830632L]

# <headingcell level=2>

# Plotting state population as a scatter graph in descending order by population

# <markdowncell>

# Purpose:  construct state_pop DataFrame to use for plotting

# <codecell>

state_pop = df[df.geog_type=='state']['POP010210'].copy()

# use sort to do in-place sort
state_pop.sort()
state_pop[:5]

# <codecell>

state_pop.order()[::-1]
state_pop.sum()

# <headingcell level=2>

# Exercise:  Produce a cumulative population graph of states

# <markdowncell>

# 
# * x value is the rank (starting with 0)
# * y value is the normalized cumulative population
# 
# Some specific values to be plotted:
# 
#     0     0.120662
#     1     0.202107
#     2     0.264871
#     3     0.325766
#     ....
#     ....
#     47    0.994199
#     48    0.996226
#     49    0.998174
#     50    1.000000
# 
# Consider using [cumsum](http://pandas.pydata.org/pandas-docs/dev/generated/pandas.Series.cumsum.html) in relation to `state_pop`.
# 
# Your graph should look something like the following:
# 
# <a href="http://www.flickr.com/photos/raymondyee/8471907573/" title="day_08_state_cumulative_normalized by Raymond Yee, on Flickr"><img src="http://farm9.staticflickr.com/8524/8471907573_5b1f7b4df5.jpg" width="367" height="249" alt="day_08_state_cumulative_normalized"></a>

# <codecell>

# FILL IN WITH YOUR CODE TO GENERATE PLOT




# <headingcell level=1>

# Let's make a simple bar graph

# <markdowncell>

# First, consider a simple example bar graph to learn from

# <codecell>

import string
num_letter_series = Series(arange(10), index=list(string.lowercase[:10]))
num_letter_series 

# <codecell>

num_letter_series.plot(kind="bar")

# <headingcell level=2>

# Exercise: Make a bar chart of state population

# <markdowncell>

# Requirement:
# 
# * states listed in descending order by population on x-axis
# * population on the y-axis
# 
# Your plot should look something like the following:
# 
# <a href="http://www.flickr.com/photos/raymondyee/8473055924/" title="day_08_state_pop_bar by Raymond Yee, on Flickr"><img src="http://farm9.staticflickr.com/8239/8473055924_02422854b9.jpg" width="368" height="369" alt="day_08_state_pop_bar"></a>

# <codecell>

# FILL IN WITH YOUR CODE TO GENERATE BAR PLOT




# <headingcell level=1>

# Exercise: Using groupby to compare aggregate populations with stated totals

# <markdowncell>

# 1. Calculate a DataFrame named `state_pop_total` that sums up the populations for all counties in the state. `state_pop_total` must be indexed on `fips_prefix`.  Hint: do a `group_by` operation on `df` and then sort by
# descending population.
# 
# 1. Calculate a DataFrame named `extracted_state_pops` that is indexed by `fips_prefix` and holds the total population
# as stated for given state in `df`.  Make `extracted_state_pops` sorted by descending population also

# <codecell>

# FILL IN WITH YOUR CODE for state_pop_total and extracted_state_pops




# <codecell>

# TEST


assert isinstance(state_pop_total, DataFrame)
assert map(unicode, list(state_pop_total.index)) == [u'06', u'48', u'36', u'12', u'17', u'42', u'39', u'26',
 u'13', u'37', u'34', u'51', u'53', u'25', u'18', u'04', u'47', u'29', u'24', u'55', 
 u'27', u'08', u'01', u'45', u'22', u'21', u'41', u'40', u'09', u'19', u'28', 
 u'05', u'20', u'49', u'32', u'35', u'54', u'31', u'16', u'15', u'23', u'33', u'44', 
 u'30', u'10', u'46', u'02', u'38', u'50', u'11', u'56']
assert set(state_pop_total.columns) == set(['POP010210'])
assert state_pop_total[:5].sum() == 113409561

# compare all the state totals
assert np.all(state_pop_total['POP010210'] == extracted_state_pops['POP010210'])

# <headingcell level=1>

# Note:  You can use a DataFrame to align indexes

# <headingcell level=2>

# Exercise:  Run the following code to make sure you know what's going on here.

# <codecell>

# Series must be sorted in same order for comparison to work -- the following is False

np.all(state_pop_total['POP010210'].order() == extracted_state_pops['POP010210'])

# <codecell>

# let's shuffle the index

import random 

shuffle_index = list(state_pop_total.index)
random.shuffle(shuffle_index)
print shuffle_index

# <codecell>

# use reindex to create a shuffled Series

shuffled_series = state_pop_total['POP010210'].reindex(index=shuffle_index)
shuffled_series[:5]

# <codecell>

#  When you insert these three Series into a common DataFrame, you can do comparisons across the columns

comp = DataFrame(index=extracted_state_pops.index)
comp['extracted'] = extracted_state_pops['POP010210']
comp['total'] = state_pop_total['POP010210']
comp['shuffle'] = shuffled_series

# <codecell>

np.all(comp['extracted'] == comp['total'])

# <codecell>

np.all(comp['shuffle'] == comp['total'])

