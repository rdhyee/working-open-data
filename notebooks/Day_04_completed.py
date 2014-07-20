# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <headingcell level=1>

# Warm up with sequences, lists

# <headingcell level=2>

# Warm-up exercise I:  verifying sum of integers calculated by (young) Gauss

# <markdowncell>

# ![C. F. Gauss](http://upload.wikimedia.org/wikipedia/commons/thumb/9/9b/Carl_Friedrich_Gauss.jpg/220px-Carl_Friedrich_Gauss.jpg)
# 
# http://mathandmultimedia.com/2010/09/15/sum-first-n-positive-integers/
# 
# >  Gauss displayed his genius at an early age. According to anecdotes, when he was in primary school, he was punished by his teacher due to misbehavior.  He was told to add the numbers from 1 to 100. He was able to compute its sum, which is 5050, in a matter of seconds.
# 
# >  Now, how on earth did he do it?
# 
# See also:
# 
# * http://en.wikipedia.org/wiki/Carl_Friedrich_Gauss#Anecdotes
# * [The Gauss Christmath Special](http://youtu.be/sxnX5_LbBDU?t=4m52s) by [Vi Hart](http://en.wikipedia.org/wiki/Vi_Hart)
# 
# **Let's verify this result in a number of ways.  Take some time now to write some code to add up 1 to 100.**
# 
# Specifically:
# 
# * make use of [range](http://docs.python.org/2/library/functions.html#range)
# * try [xrange](http://docs.python.org/2/library/functions.html#xrange)
# * try an explicit loop vs `sum`
# * bonus:  try [itertool.count](http://docs.python.org/2/library/itertools.html#itertools.count) and [itertool.islice](http://docs.python.org/2/library/itertools.html#itertools.islice) -- these functions are Python *iterators*. 
# * See [Build a Basic Python Iterator](http://stackoverflow.com/a/24377/7782) and 
# [The Python yield keyword explained](http://stackoverflow.com/questions/231767/the-python-yield-keyword-explained)
# 
# 
# **Beware:  in ipython w/ pylab mode, `sum` might be overwritten by numpy's sum -- use `__builtin__.sum` if you want http://docs.python.org/2/library/functions.html#sum as opposed to http://docs.scipy.org/doc/numpy/reference/generated/numpy.sum.html** 

# <codecell>

%pylab inline

# <codecell>

# using loop

n = 100

s = 0L
for i in xrange(n+1):
    s += i
print s

# <codecell>

# range
print range(101)
sum(range(101))

# <codecell>

# xrange
sum(xrange(101))

# <codecell>

from itertools import islice, count

c = count(0, 1)

# <codecell>

# look at how count() works by repetively calling c.next()
print c.next()
print c.next()

# <codecell>

# count
__builtin__.sum(islice(count(0,1), 101L))

# <codecell>

import string

def alpha1():
    m = list(string.lowercase)
    while m:
        yield m.pop(0)
    

# <codecell>

import string
k = (s for s in list(string.lowercase))
list(k)

# <codecell>

def my_count(start, step):
    n = start
    while True:
        yield n
        n += step
        
__builtin__.sum(islice(my_count(0,1), 101L))

# <markdowncell>

# $T_n= \sum_{k=1}^n k = 1+2+3+ \dotsb +n = \frac{n(n+1)}{2} = {n+1 \choose 2}$

# <codecell>

from itertools import islice

def triangular():
    n = 1
    i = 1
    while True:
        yield n
        i +=1
        n += i

# <codecell>

for i, n in enumerate(islice(triangular(), 10)):
    print i+1, n

# <codecell>

list(islice(triangular(), 100))[-1]

# <codecell>

list(islice(triangular(),99,100))[0]

# <headingcell level=2>

# Warm Up Exercise II: Wheat and chessboard problem

# <markdowncell>

# http://en.wikipedia.org/wiki/Wheat_and_chessboard_problem :
# 
# > If a chessboard were to have wheat placed upon each square such that one grain were placed on the first square, two on the second, four on the third, and so on (doubling the number of grains on each subsequent square), how many grains of wheat would be on the chessboard at the finish?
# 
# > The total number of grains equals 18,446,744,073,709,551,615, which is a much higher number than most people intuitively expect.
# 
# * try using [pow](http://docs.python.org/2/library/functions.html#pow)

# <codecell>

# Legend of the Chessboard YouTube video

from IPython.display import YouTubeVideo
YouTubeVideo('t3d0Y-JpRRg')

# <codecell>

# generator comprehension

k  = (pow(2,n) for n in xrange(64))
k.next()

# <codecell>

__builtin__.sum((pow(2,n) for n in xrange(64)))

# <codecell>

pow(2,64) -1

# <headingcell level=1>

# Slicing/Indexing Review

# <markdowncell>

# http://stackoverflow.com/a/509295/7782
# 
# Use on any of the **sequence** types ([python docs on sequence types](http://docs.python.org/2/library/stdtypes.html#sequence-types-str-unicode-list-tuple-bytearray-buffer-xrange)):
# 
# > There are seven sequence types: strings, Unicode strings, lists, tuples, bytearrays, buffers, and xrange objects.
# 
# The use of square brackets are for accessing *slices* of sequence.

# <markdowncell>

# Let's remind ourselves of how to use slices
# 
# * `s[i]`
# * `s[i:j]`
# * `s[i:j:k]`
# * meaning of negative indices
# * 0-base counting
# 

# <codecell>

m = range(10)
m

# <codecell>

m[0]

# <codecell>

m[-1]

# <codecell>

m[::-1]

# <codecell>

m[2:3]

# <codecell>

import string
alphabet = string.lowercase

alphabet

# <codecell>

# 13 letter of the alphabet
alphabet[12]

# <markdowncell>

# **We will revisit generalized slicing in NumPy.**

# <headingcell level=1>

#  Import/naming conventions and pylab mode

# <markdowncell>

# <http://my.safaribooksonline.com/book/programming/python/9781449323592/1dot-preliminaries/id2699702>
# 
#     import numpy as np
#     import pandas as pd
#     import matplotlib.pyplot as plt
#     from pandas import Series, DataFrame
#     
# These imports done for you in `pylab` mode.
# 
# ## pylab mode
# 
#     ipython --help
#     
# yields
# 
#     --pylab=<CaselessStrEnum> (InteractiveShellApp.pylab)
#         Default: None
#         Choices: ['tk', 'qt', 'wx', 'gtk', 'osx', 'inline', 'auto']
#         Pre-load matplotlib and numpy for interactive use, selecting a particular
#         matplotlib backend and loop integration.

# <codecell>

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pandas import Series, DataFrame

# <headingcell level=1>

# NumPy

# <markdowncell>

# <http://www.numpy.org/>:
# 
# NumPy is the **fundamental package for scientific computing with Python**. It contains among other things:
# 
# * a powerful N-dimensional array object [let's start with 1 and 2 dimensions]
# * sophisticated (**broadcasting**) functions [what is *broadcasting*?]
# * tools for integrating C/C++ and Fortran code [why useful?]
# * useful linear algebra, Fourier transform, and random number capabilities
# 
# Besides its obvious scientific uses, NumPy can also be used as an efficient
# multi-dimensional container of **generic data**. **Arbitrary data-types** can be
# defined. This allows NumPy to seamlessly and speedily integrate with a wide
# variety of databases.
# 
# See `PfDA`, Chapter 4

# <headingcell level=2>

# ndarray.ndim, ndarray.shape

# <codecell>

# zero-dimensions

a0 = np.array(5)
a0

# <markdowncell>

# use [shape](http://docs.scipy.org/doc/numpy/reference/generated/numpy.ndarray.shape.html) to get a tuple of array dimensions

# <codecell>

a0.ndim, a0.shape

# <codecell>

# 1-d array
a1 = np.array([1,2])
a1.ndim, a1.shape

# <codecell>

# 2-d array

a2 = np.array(([1,2], [3,4]))
a2.ndim, a2.shape

# <headingcell level=2>

# dtype:  type of given ndarray

# <codecell>

a2.dtype

# <headingcell level=2>

# np.arange

# <markdowncell>

# [arange](http://docs.scipy.org/doc/numpy/reference/generated/numpy.arange.html#numpy.arange) is one instance of [`ndarray` creating function in NumPy](http://docs.scipy.org/doc/numpy/reference/routines.array-creation.html)
# 
# Compare to `xrange`.

# <codecell>

type(arange(10))

# <codecell>

for k in arange(10):
    print k

# <codecell>

list(arange(10)) == list(xrange(10))

# <headingcell level=2>

# NumPy.ndarray.reshape

# <codecell>

#how to map 0..63 -> 2x2 array
a3 = np.arange(64).reshape(8,8)
a3

# <codecell>

a3[1,2]

# <codecell>

for i in range(8):
    for j in range(8):
        if a3[i,j] != i*8 + j:
            print i, j

# <markdowncell>

# ##scalar multiplication
# 
# example of [broadcasting](http://docs.scipy.org/doc/numpy/user/basics.broadcasting.html):
# 
# > The term broadcasting describes how numpy treats arrays with different shapes during arithmetic operations. Subject to certain constraints, the smaller array is “broadcast” across the larger array so that they have compatible shapes. Broadcasting provides a means of vectorizing array operations so that looping occurs in C instead of Python. It does this without making needless copies of data and usually leads to efficient algorithm implementations. There are, however, cases where broadcasting is a bad idea because it leads to inefficient use of memory that slows computation.

# <codecell>

2*a3

# <headingcell level=2>

# add 2 to all elements in a3

# <codecell>

a3+2

# <headingcell level=2>

# sorting

# <codecell>

# reverse sort -- best way?
#http://stackoverflow.com/a/6771620/7782

np.sort(arange(100))[::-1]

# <headingcell level=2>

# Boolean slice:  important novel type of slicing

# <markdowncell>

# **This stuff is a bit tricky** (see PfDA, pp. 89-92)
# 
# Consider example of picking out whole numbers less than 20 that are evenly divisible by 3.  Generate a list of such numbers

# <codecell>

# list comprehension

[i for i in xrange(20) if i % 3 == 0]

# <codecell>

a3 = arange(20) 
a3

# <codecell>

# basic indexing

print a3[0]
print a3[::-1]
print a3[2:5]

# <codecell>

np.mod(a3, 3)

# <codecell>

np.mod(a3, 3) == 0

# <codecell>

divisible_by_3 = np.mod(a3, 3) == 0

# <codecell>

a3[divisible_by_3]

# <codecell>

# if you want to understand this in terms of the overloaded operators -- don't worry if you don't get this.
a3.__getitem__(np.mod(a3,3).__eq__(0))

# <headingcell level=2>

# Exercise:  Calculate a series that holds all the squares less than 100

# <markdowncell>

# Use arange, np.sqrt, [astype](http://docs.scipy.org/doc/numpy/reference/generated/numpy.ndarray.astype.html)

# <codecell>

a4 = arange(100)
a4sqrt = np.sqrt(a4)
a4[a4sqrt == a4sqrt.astype(np.int)]

# <headingcell level=2>

# We will come back to indexing later.

# <markdowncell>

# http://docs.scipy.org/doc/numpy/reference/arrays.indexing.html

# <headingcell level=1>

# Pandas

# <headingcell level=2>

# pandas.Series

# <markdowncell>

# Make a series out of an array

# <codecell>

s1 = Series(arange(5))

# <markdowncell>

#   confirm that the type of s1 is  what you would expect

# <codecell>

type(s1)

# <markdowncell>

# show that the series is also an array

# <codecell>

s1.ndim, isinstance(s1, np.ndarray)

# <codecell>

s1.index

# <codecell>

import string
allTheLetters = string.lowercase
allTheLetters

# <codecell>

s2 = Series(data=arange(5), index=list(allTheLetters)[:5])
s2

# <codecell>

s2.index

# <markdowncell>

# http://my.safaribooksonline.com/book/programming/python/9781449323592/5dot-getting-started-with-pandas/id2828378 :
# 
# > Compared with a regular NumPy array, you can use values in the index when selecting single values or a set of values

# <codecell>

# can use both numeric indexing and the labels
s2[0], s2['a']

# <codecell>

for i in range(len(s2)):
    print i, s2[i]

# <markdowncell>

# it is possible conflict in indexing -- consider

# <codecell>

s3 = Series(data=['albert', 'betty', 'cathy'], index=[3,1, 0])
s3

# <codecell>

s3[0], list(s3)[0]

# <markdowncell>

# but slicing works to return specific numeric index

# <codecell>

s3[::-1]

# <codecell>

for i in range(len(s3)):
    print i, s3[i:i+1]

# <codecell>

s3.name = 'person names'
s3.name

# <codecell>

s3.index.name = 'confounding label'
s3.index.name

# <codecell>

s3

# <markdowncell>

# Important points remaining:
# 
# * "NumPy array operations, such as filtering with a boolean array, scalar multiplication, or applying math functions, will preserve the index-value link"
# * "Another way to think about a Series is as a fixed-length, ordered dict, as it is a mapping of index values to data values. It can be substituted into many functions that expect a dict"

# <headingcell level=2>

# Gauss & Chess revisited, using Series

# <markdowncell>

# You get some nice `matplotlib` integration via pandas

# <codecell>

# Gauss addition using np.arange, Series 

from pandas import Series
Series(arange(101).cumsum()).plot()

# <codecell>

from pandas import Series
Series((pow(2,k) for k in xrange(64)), dtype=np.float64).cumsum().plot()

# <headingcell level=2>

# Wheat and Chessboard w/ NumPy

# <markdowncell>

# http://docs.scipy.org/doc/numpy/reference/ufuncs.html

# <codecell>

2*ones(64, dtype=np.int)

# <codecell>

arange(64)

# <codecell>

sum(np.power(2, arange(64, dtype=np.uint64)))

# <codecell>

sum(np.power(2*ones(64, dtype=np.uint64), arange(64))) 

# <codecell>

precise_ans = sum([pow(2,n) for n in xrange(64)])
np_ans = sum(np.power(2*ones(64, dtype=np.uint64), arange(64)))

precise_ans, np_ans


# <codecell>

# Raise an assertion if two items are not equal up to desired precision.
np.testing.assert_almost_equal(precise_ans, np_ans) is None

# <headingcell level=1>

# File Dependency Check for Census calculation

# <markdowncell>

# Here we check to make sure that the expected files are in place.
# 
# This notebook assumes relative location of files as laid out in https://github.com/rdhyee/working-open-data
# 

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
    print abs_fname, os.path.exists(abs_fname)
    

# <markdowncell>

#  You can download git repo as zip file if you are having problems with github
# 
# <img src="https://raw.github.com/rdhyee/working-open-data/master/lectures/images/download_repo_as_zip.jpg" />

# <headingcell level=1>

# Let's do the pandas related imports

# <codecell>

import pandas as pd
from pandas import Series, DataFrame

# <headingcell level=1>

# Getting more out of iPython notebook

# <markdowncell>

# *PfDA*, p. 55 -- Table 3-2
# 
# http://my.safaribooksonline.com/book/programming/python/9781449323592/3dot-ipython-an-interactive-computing-and-development-environment/id2774782#ipython_magic_table

# <headingcell level=1>

# Census Quickfacts

# <codecell>

# use head on Mac/linuc to look at file

fips_path = file_path("fips")
!head $fips_path

# <headingcell level=2>

# trying out by hand the construction of a simple DataFrame to see what loading a list of dict into DataFrame gets us

# <codecell>

df1 = DataFrame([{'fips':'00000', 'geog_entity':'UNITED STATES'}, 
              {'fips':'01000', 'geog_entity':'ALABAMA'},
              ])
df1

# <codecell>

# check type of df1
type(df1)

# <codecell>

# column headings

df1.columns

# <codecell>

# index -- ascribed automatically since we didn't explicitly specify labels
df1.index

# <markdowncell>

# We can use [`set_index`](http://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.set_index.html#pandas.DataFrame.set_index) to makes fips the index

# <codecell>

# http://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.set_index.html#pandas.DataFrame.set_index
# p. 150
df1.set_index('fips', inplace=True, drop=True)

# <codecell>

# now check the index
df1.index

# <codecell>

# to access row with index of 01000
df1.ix['01000'] 

# <codecell>

# to read off the geog_entity column
df1['geog_entity']

# <codecell>

# look at how we can do row slices
df1.ix[0:1]

# <codecell>

# get rows in reverse order
df1.ix[::-1]

# <markdowncell>

# Create the index explicitly in instantiation of the simple DataFrame

# <codecell>

df2 = DataFrame(data = [{'geog_entity':'UNITED STATES'}, 
                {'geog_entity':'ALABAMA'},
                ], index = ['00000','01000'])
df2

# <codecell>

# note index name is empty
df2.index.name is None

# <codecell>

# set index name
df2.index.name = 'fips'
df2

# <headingcell level=2>

# Exercise:  Complete this code to create fips_df from the fips file

# <codecell>

import codecs
from itertools import islice

from pandas import Series, DataFrame

f = codecs.open(file_path("fips"), encoding='iso-8859-1')

fips_list = list()

for row in islice(f, None):
    fips_list.append({'fips': row[:5], 'geog_entity': row[6:-1]})
    
fips_df = DataFrame(fips_list)
fips_df

# <codecell>

# display the first 5 rows
fips_df[:5]

# <headingcell level=2>

# let's try using read_table directly to read in fips code

# <codecell>

import codecs
from itertools import islice

import pandas as pd
from pandas import Series, DataFrame

f = codecs.open(file_path("fips"), encoding='iso-8859-1')

fips_df2 = pd.read_table(f, header=None,names=['row'])

# show first five rows
fips_df2[:5]


# <headingcell level=3>

# Exercise: create a fips column

# <markdowncell>

# hint:  consider using `fips_df2.row.str[:]` and see what happens if you use
# 
#     fips_df2["junk"] = 'hello'
# 
# BTW, you can delete columns  -- e.g.,
# 
#     del fips_df2["junk"] 

# <codecell>

fips_df2["fips"] = fips_df2.row.str[:5]

# <codecell>

# show first five rows
fips_df2[:5]

# <headingcell level=3>

# Exercise: Likewise, create the geog_entity column and get rid of row column

# <codecell>

fips_df2["geog_entity"] = fips_df2.row.str[6:]
fips_df2[:5]

# <codecell>

del fips_df2["row"]

# <codecell>

fips_df2[:5]

# <codecell>

# this is a check that you have the right columns

assert set(fips_df2.columns) == set(['fips', 'geog_entity'])
assert len(fips_df2) == 3195

# <headingcell level=3>

# Now set the fips to be the index

# <codecell>

fips_df2.set_index('fips', inplace=True, drop=True)

# <codecell>

# print out first five rows
fips_df2[:5]

# <codecell>

fips_df2.ix['00000']

# <headingcell level=3>

# Note:  see how to pull out country + states

# <codecell>

bool_index = Series(fips_df2.index).str[-3:] == '000'

# <codecell>

Series(fips_df2.index,index=fips_df2.index).str[-3:] == '000'

# <codecell>

bool_index.index

# <codecell>

fips_df2.index

# <codecell>

Series(fips_df2.index).str[-3:] == '000'

# <codecell>

# first 5 rows
fips_df2[Series(fips_df2.index, index=fips_df2.index).str[-3:] == '000'][:5]

# <codecell>

len(fips_df2[Series(fips_df2.index, index=fips_df2.index).str[-3:] == '000'])

# <codecell>

# check type
isinstance(fips_df2.index, pd.Index)

# <codecell>

# can create a Boolean slice to pull out a country
is_country = fips_df.fips.str[:] == '00000'

# <codecell>

fips_df[is_country]

# <headingcell level=3>

# Exercise:  create a Boolean index `is_state` to pull out states and a DataFrame `states_df` to hold the states + DC; also write `is_county` to pull out counties

# <markdowncell>

# Hints:
# 
# * Recall how to distinguish states fips -- end in '000' but is not '00000' (which is the US code)
# * use can use `&` to do a boolean `and` on Boolean indices -- (see `PfDA`, p. 91)

# <codecell>

# how about states?
# make use of 
# http://proquest.safaribooksonline.com/book/programming/python/9781449323592/7dot-data-wrangling-clean-transform-merge-reshape/id2801165

is_state = (fips_df.fips.str[-3:] == '000') & (fips_df.fips.str[:] != '00000')
is_county = fips_df.fips.str[-3:] != '000'

states_df = fips_df[is_state]
print len(states_df)
states_df[:5]

# <headingcell level=3>

# Check whether is_state and states_df look correct

# <codecell>

assert set(is_state.value_counts().iteritems()) == set([(True, 51), (False, 3144)])

# <codecell>

assert set(states_df["geog_entity"]) == set([u'VERMONT',
     u'GEORGIA', u'IOWA', u'KANSAS', u'FLORIDA', u'VIRGINIA', u'NORTH CAROLINA',
     u'HAWAII', u'NEW YORK', u'CALIFORNIA', u'ALABAMA', u'IDAHO', u'DELAWARE',
     u'ALASKA', u'ILLINOIS', u'SOUTH DAKOTA', u'CONNECTICUT', u'MONTANA',
     u'MASSACHUSETTS', u'NEW HAMPSHIRE', u'MARYLAND', u'NEW MEXICO',
     u'MISSISSIPPI', u'TENNESSEE', u'COLORADO', u'NEW JERSEY', u'UTAH',
     u'MICHIGAN', u'WEST VIRGINIA', u'WASHINGTON', u'MINNESOTA', u'OREGON',
     u'WYOMING', u'OHIO', u'SOUTH CAROLINA', u'INDIANA', u'NEVADA',
     u'LOUISIANA', u'NEBRASKA', u'ARIZONA', u'WISCONSIN', u'NORTH DAKOTA',
     u'PENNSYLVANIA', u'OKLAHOMA', u'KENTUCKY', u'RHODE ISLAND', u'DISTRICT OF COLUMBIA',
     u'ARKANSAS', u'MISSOURI', u'TEXAS', u'MAINE'])

# <codecell>

assert set(is_county.value_counts().iteritems()) == set([(False, 52), (True, 3143)])

# <headingcell level=2>

# Now it's time to work with the population dataset

# <headingcell level=3>

# remind ourselves of what's in the dataset by reading it into a dict

# <codecell>

import csv
import codecs
import pandas as pd
from pandas import DataFrame, Series
from itertools import islice

f = codecs.open(file_path("dataset"), encoding='iso-8859-1')

reader = csv.DictReader(f)
dataset = dict([(row["fips"], row) for row in islice(reader, None)])

f.close()

# <codecell>

# print out entry for USA

print dataset['00000']

# <codecell>

# make sure we have the right 2010 census population for the USA

assert dataset['00000']['POP010210'] == '308745538'

# <headingcell level=3>

# let's use pd.read_csv to read in file -- there's a bit of tricky type conversion issues here.

# <codecell>

# let's try pd.read_csv 
# how to give hints about data type to pd.read_csv?

import codecs

# read data in and merge with fips_df

#dtype = [('fips', 'S'), ('POP010210', 'i')]
# problems with string conversion when I try to explicitly parse fips as a np.string_
# dtype = {'fips':np.string_}
# possibly relevant sections of the code:

# v0.10.1: https://github.com/pydata/pandas/tree/v0.10.1
# https://github.com/pydata/pandas/blob/v0.10.1/pandas/io/parsers.py
# https://github.com/pydata/pandas/blob/v0.10.1/pandas/src/parser.pyx#L897 -> _convert_with_dtype

# let's try object for fips and int for POP010210
dtype = {'fips':np.object, 'POP010210':np.int}

f = codecs.open(file_path("dataset"), encoding='iso-8859-1')
dataset_df = pd.read_csv(f, dtype=dtype)

# <codecell>

# confirm data types for fips, which should not be convered to int
dataset_df.fips.dtype, dataset_df.POP010210.dtype

# <codecell>

# read off US population
dataset_df[is_country].ix[0]['POP010210']

# <codecell>

# 3 most populous entities 
# http://pandas.pydata.org/pandas-docs/dev/generated/pandas.DataFrame.sort_index.html
dataset_df.sort_index(by='POP010210')[-1:-4:-1][["fips", "POP010210"]]

# <headingcell level=2>

# Merge fips w/ dataset

# <codecell>

# before doing merge,list expected columns

'fips' in fips_df.columns, 'fips' in dataset_df.columns

# <codecell>

# PfDA, p. 28
df = pd.merge(fips_df, dataset_df)

# <codecell>

df.sort_index(by='POP010210')[-1:-5:-1][["fips", "geog_entity", "POP010210"]]

# <headingcell level=3>

# Exercise: make a DataFrame called state_pop of 51 state-like entities that has fips, geog_entity, POP010210 columns, sorted by 2010 census in descending pop

# <codecell>

state_pop = df[is_state][["fips", "geog_entity", "POP010210"]].sort_index(by='POP010210')[::-1]
state_pop[:5]

# <codecell>

# check state_pop behavior

assert state_pop.shape  == (51, 3)
assert set(state_pop.columns) == set(['POP010210', 'fips', 'geog_entity'])
assert list(state_pop[:5]["geog_entity"]) == [u'CALIFORNIA', u'TEXAS', u'NEW YORK', u'FLORIDA', u'ILLINOIS']
assert state_pop[:5]["POP010210"].sum() == 113409561

# <codecell>

# add up all the states to match US population

assert state_pop["POP010210"].sum() == df[is_country]["POP010210"].sum()

# <codecell>

sum(df[is_country]['POP010210']), sum(df[is_state]['POP010210']), sum(df[is_county]['POP010210'])

# <headingcell level=2>

# Exercise:  write function counties_for_state to return a Boolean index for a fiven state prefix or fips code

# <markdowncell>

# e.g 
# 
#     df[counties_for_state('06')]
# 
# should be a DataFrame with CA counties

# <codecell>

def counties_for_state(state):
    return (df.fips.str[:2] == state[:2]) & (df.fips.str[-3:] != '000') 

# <codecell>

assert set(df[counties_for_state('06')]["geog_entity"]) == set([u'Nevada County, CA',
     u'Alameda County, CA', u'Kings County, CA', u'Ventura County, CA',
     u'El Dorado County, CA', u'San Joaquin County, CA', u'Alpine County, CA',
     u'San Luis Obispo County, CA', u'Modoc County, CA', u'Colusa County, CA',
     u'Stanislaus County, CA', u'Sonoma County, CA', u'Tulare County, CA',
     u'Shasta County, CA', u'Yolo County, CA', u'Placer County, CA', u'Glenn County, CA',
     u'Sacramento County, CA', u'San Francisco County, CA',
     u'Madera County, CA', u'Imperial County, CA', u'Plumas County, CA',
     u'San Mateo County, CA', u'Riverside County, CA', u'Calaveras County, CA',
     u'Napa County, CA', u'Mendocino County, CA', u'Mariposa County, CA',
     u'Santa Barbara County, CA', u'Inyo County, CA', u'Butte County, CA',
     u'Trinity County, CA', u'Los Angeles County, CA', u'Lassen County, CA',
     u'Yuba County, CA', u'Amador County, CA', u'Marin County, CA', u'Humboldt County, CA', 
     u'Merced County, CA', u'Lake County, CA', u'San Diego County, CA',
     u'Monterey County, CA', u'Sutter County, CA', u'Solano County, CA',
     u'Tuolumne County, CA', u'San Bernardino County, CA', u'Fresno County, CA',
     u'Santa Cruz County, CA', u'San Benito County, CA', u'Contra Costa County, CA', 
     u'Orange County, CA', u'Del Norte County, CA', u'Mono County, CA',
     u'Siskiyou County, CA', u'Kern County, CA', u'Sierra County, CA', u'Tehama County, CA',
     u'Santa Clara County, CA'])

# <headingcell level=1>

# Now we are ready to tally up all states w/ their counties

# <codecell>

for (k, s) in df[is_state][['fips', 'geog_entity', 'POP010210']].iterrows():
    print s["fips"], s["geog_entity"], s["POP010210"] == df[counties_for_state(s["fips"])]['POP010210'].sum()

# <headingcell level=2>

# Do this tally in a slightly different way

# <codecell>

# http://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.set_index.html#pandas.DataFrame.set_index
# p. 150
df.set_index('fips', inplace=True, drop=False)

# <codecell>

for k in df[is_state]['fips']:
    print k, df.ix[k]["geog_entity"], df.ix[k]["POP010210"] == sum(df[counties_for_state(k)]['POP010210'])

# <codecell>

# does order of A== B vs B== A matter -- shouldn't

state = '06000'
k0 = df.fips.str[:2] == state[:2]
type(k0)
k1 = state[:2] == df.fips.str[:2]
print type(k0), type(k1)
print k0.value_counts()
print k1.value_counts()
print np.all(k0 == k1)

# <headingcell level=1>

# Addendum: ties to operator overloading in Python -- read beyond this point only if really interested!

# <codecell>

n0 = 5
n0 == 5

# <markdowncell>

# Now I thought I'd be able to use a `n0.__eq__(5)` but nope -- it's complicated -- see http://stackoverflow.com/questions/2281222/why-when-in-python-does-x-y-call-y-eq-x#comment2254663_2282795

# <codecell>

try:
    n0.__eq__(5)
except Exception as e:
    print e

# <markdowncell>

# can do: `int.__cmp__(x)`

# <codecell>

(n0.__cmp__(4), n0.__cmp__(5), n0.__cmp__(6))

# <markdowncell>

# how about ndarray?

# <codecell>

arange(5) == 2 

# <codecell>

# 
# http://docs.scipy.org/doc/numpy/reference/generated/numpy.array_equal.html
np.array_equal(arange(5) == 2 , arange(5).__eq__(2))

# <headingcell level=2>

# Appendix: underlying mechanics of slicing

# <markdowncell>

# Useful if you want to understand how the slicing syntax really works.

# <codecell>

isinstance([1,2], list)

# <codecell>

isinstance(arange(5), list) # what does that mean -- could still be list-like

# <codecell>

l1 = range(5)

# <codecell>

type(l1)

# <codecell>

l1[0], l1.__getitem__(0), l1[0] == l1.__getitem__(0)

# <codecell>

l1[::-1], l1.__getitem__(slice(None, None, -1))

# <codecell>

ar1 = arange(5)
ar1[3], ar1.__getitem__(3)


# <codecell>

ar1 == 2

# <codecell>

ar1[ar1 == 2].shape

# <codecell>

ar1.__eq__(2)

# <codecell>

ar1.__getitem__(slice(2, 4, None))

# <codecell>

slice(ar1.__eq__(2), None, None)

# <codecell>

ar1.__getitem__(ar1.__eq__(2))

# <codecell>

ar1[:2], ar1.__getitem__(slice(2))

# <codecell>

ar1 + 7

# <codecell>

ar1.__add__(7)

# <codecell>

min(ar1 + 7)

# <codecell>

alphabet[:]

