# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <headingcell level=1>

# Goals

# <markdowncell>

# To parse text files with fixed columns such as [Census DataDict.txt](https://raw.github.com/rdhyee/working-open-data/master/data/census/DataDict.txt)

# <markdowncell>

# Reading off the columns
#  
# * 0, 8
# * 10, 111
# * 115, 117
# * 122
# * 129, 137
# * 144, 149
# * 153, 161
# * 164, 169
#  
# [u'Data_Item', u'Item_Description', u'Unit', u'Decimal', u'US_Total', u'Minimum', u'Maximum', u'Source']

# <headingcell level=1>

# Let's use requests to read file from github

# <markdowncell>

# Hint:  if you use requests to read the file, you may need to turn verify off for requests.get: http://stackoverflow.com/questions/10667960/python-requests-throwing-up-sslerror

# <codecell>

from itertools import islice
import requests
import StringIO
import os

cafile = os.path.join(os.pardir, "data/cacert.pem")
datadict_url = "https://raw.github.com/rdhyee/working-open-data/5ef3932b4ff7cadf1f06ca01eb852ad71361894a/data/census/DataDict.txt"
r = requests.get(datadict_url, verify=cafile)

f = StringIO.StringIO(r.content.decode("iso-8859-1"))

# <codecell>

r.text

# <headingcell level=1>

# Parse by counting off the column widths and parsing

# <codecell>

import os
import codecs
from itertools import islice, izip
from pandas import DataFrame

# <codecell>

datadict_path = os.path.join(os.pardir, "data/census/DataDict.txt")

# f = islice(codecs.open(datadict_path, mode="rU", encoding="iso-8859-1"), None)

cafile = os.path.join(os.pardir, "data/cacert.pem")
datadict_url = "https://raw.github.com/rdhyee/working-open-data/5ef3932b4ff7cadf1f06ca01eb852ad71361894a/data/census/DataDict.txt"
r = requests.get(datadict_url, verify=cafile)

f = StringIO.StringIO(r.content.decode("iso-8859-1"))

header_row = f.next()
header_row.split()

headers = [u'Data_Item',
 u'Item_Description',
 u'Unit',
 u'Decimal',
 u'US_Total',
 u'Minimum',
 u'Maximum',
 u'Source']

column_boundaries = [(0, 8),
  (10, 111),
  (115, 117),
  (122, 122),
  (129, 137),
  (144, 149),
  (153, 161),
  (164, 169)
]

header_to_columns = dict(izip(headers, column_boundaries))

# skip 2nd row -- exceptional

rows = islice(f, 1, None)
parsed_rows = []

for row in rows:
    row_dict = {}
    for (header, bound) in header_to_columns.iteritems():
        row_dict[header] = row[bound[0]:bound[1]+1]
    parsed_rows.append(row_dict)
    
data_dict_df = DataFrame(parsed_rows)

# <codecell>

# TEST

assert set(data_dict_df.columns) == set([u'Decimal',
     u'Maximum',
     u'Source',
     u'Minimum',
     u'Unit',
     u'US_Total',
     u'Data_Item',
     u'Item_Description'])

assert set(data_dict_df["Data_Item"]) == set([u'RHI125211',
     u'SBO415207', u'VET605211', u'RHI225211', u'PVY020211', u'HSD310211',
     u'POP645211', u'EDU635211', u'EDU685211', u'RHI625211', u'SBO215207',
     u'PST045212', u'SBO015207', u'POP715211', u'PST120211', u'PST120212',
     u'POP010210', u'PST045211', u'SBO315207', u'POP060210', u'RHI425211',
     u'POP815211', u'HSD410211', u'HSG495211', u'BZA010210', u'LFE305211',
     u'BZA110210', u'AGE775211', u'HSG096211', u'RHI525211', u'LND110210',
     u'PST040210', u'RHI825211', u'BZA115210', u'NES010210', u'MAN450207',
     u'AGE135211', u'RTN131207', u'RHI725211', u'BPS030211', u'INC110211',
     u'AGE295211', u'SBO115207', u'INC910211', u'RHI325211', u'WTN220207',
     u'HSG445211', u'SBO515207', u'AFN120207', u'RTN130207', u'HSG010211',
     u'SEX255211', u'SBO001207'])

# <codecell>

k = np.array(list('hi there! '), np.dtype('U1'))

# <codecell>

k.dtype

# <codecell>

len(k)

# <codecell>

k[0]

# <codecell>

k[1]

# <codecell>

np.char.isspace(k)

# <codecell>

r1 = "12 123 456"
r2 = "23 455  xx"

a1= np.frombuffer(r1, dtype='S1')
a2 = np.frombuffer(r1, dtype='S1')


# <codecell>

np.char.isspace(a1) & np.char.isspace(a2)

# <codecell>

u"1".encode('utf-8')

# <codecell>

rows = ["12 123 456",
        "23 455  xx",
        " 4 789 333"]

m = np.char.isspace(np.vstack((np.frombuffer(row, dtype='S1') for row in rows)))

# <codecell>

m

# <codecell>

m.shape

# <codecell>

import pandas as pd

cols_isspace = pd.Series([np.all(col) for col in m.T])

# <codecell>

cols_isspace[cols_isspace].index

# <codecell>

m

# <codecell>

np.where(np.all(m, 0))

# <headingcell level=1>

# parsing using sets

# <codecell>

from itertools import islice, izip, groupby
import re
import os
import codecs
import operator

DATA_DIR = os.path.join(os.pardir, "data")

f = codecs.open(os.path.join(DATA_DIR, "census/DataDict.txt"), encoding="iso-8859-1")

f_sliced = islice(f, None)

head_row = f_sliced.next()
headers = head_row.split()

print headers

# Actually, Unit should be broken off from Decimal

# skip the second row also
header2 = f_sliced.next()

# read in all the rows

rows = list([r[:-1] for r in islice(f_sliced,None)])

# What's the max length of rows?

max_len = max([len(row) for row in rows])
print max_len

# loop through all rows, looking for which columns have spaces exclusively

cols_with_space = set(range(max_len))

for row in rows:
    cols_with_space_in_row = set([m.start() for m in re.finditer(' ', row)])
    cols_with_space.intersection_update(cols_with_space_in_row)

cols_with_data = set(range(max_len)) - cols_with_space
# print sorted(cols_with_data)

# http://code.activestate.com/recipes/496682-make-ranges-of-contiguous-numbers-from-a-list-of-i/#c2

ranges = [map(operator.itemgetter(1), g) for k, g in groupby(enumerate(sorted(cols_with_data)), lambda (i,x):i-x) ]
print [(r[0], r[-1]+1) for r in ranges]

for row in rows:
    print [row[r[0]:r[-1]+1].strip() for r in ranges]

# <markdowncell>

# how to cast into standard size string?
# 

# <codecell>

s = "hello there folks"
print [i for (i, k) in enumerate(list(s)) if k == ' ']

# http://stackoverflow.com/a/4664889/7782

import re
print [m.start() for m in re.finditer(' ', s)]

# <codecell>

import sets
a = set(range(10))
a.intersection_update([2,3])
a

# <codecell>

# http://code.activestate.com/recipes/496682-make-ranges-of-contiguous-numbers-from-a-list-of-i/#c2

from itertools import groupby
import operator

data = [ 1,  4,5,6, 10, 15,16,17,18, 22, 25,26,27,28]
for k, g in groupby(enumerate(data), lambda (i,x):i-x):
       print map(operator.itemgetter(1), g)

# <codecell>

# masking
# http://docs.scipy.org/doc/numpy/reference/maskedarray.generic.html

import numpy as np
import numpy.ma as ma

x = np.array([1, 2, 3, -1, 5])
mx = ma.masked_array(x, mask=[0, 0, 0, 1, 0])

mx

# <codecell>

mx.count()

# <codecell>

# np.ma.clump_masked

[mx[s].data for s in np.ma.clump_unmasked(mx)]

# <codecell>

# http://stackoverflow.com/a/14606271/7782

import numpy as np
nan = np.nan

def using_clump(a):
    return [a[s] for s in np.ma.clump_unmasked(np.ma.masked_invalid(a))]

x = [nan,nan, 1 , 2 , 3 , nan, nan, 10, 11 , nan, nan, nan, 23, 1, nan, 7, 8]

using_clump(x)

# <codecell>

from itertools import islice, izip, groupby
import re
import os
import codecs
import operator
import pandas as pd

DATA_DIR = os.path.join(os.pardir, "data")

f = codecs.open(os.path.join(DATA_DIR, "census/DataDict.txt"), encoding="iso-8859-1")

f_sliced = islice(f, None)

head_row = f_sliced.next()
headers = head_row.split()

print headers

# Actually, Unit should be broken off from Decimal

# skip the second row also
header2 = f_sliced.next()

# read in all the rows

rows = list([r[:-1] for r in islice(f_sliced,None)])

# What's the max length of rows?

max_len = max([len(row) for row in rows])
print max_len, len(rows)

rows_array = np.vstack((np.array(list(row), dtype='S1') for row in rows))

m = np.char.isspace(rows_array)
print m.shape
mask = np.all(m,0)
#mask = np.where(np.all(m,0))
mask

# mask == np.array([np.all(col) for col in m.T])

df = pd.DataFrame([["".join(list(rows_array_row[s])).strip() for s in np.ma.clump_unmasked(np.ma.array(rows_array_row, mask =mask))] for rows_array_row in rows_array],
       columns = [u'Data_Item', u'Item_Description', u'Unit', u'Decimal', u'US_Total', u'Minimum', u'Maximum', u'Source'])
df

# <codecell>

# compare rows / m

from itertools import izip

#for (i, (r0, m0)) in enumerate(izip(rows, m)):
#    print r0, m0
#    # print i, np.all([c == ' ' for c in r0] == m0)

rnum = 1
all([c == ' ' for c in rows[rnum]] == m[rnum])

[c == ' ' for c in rows[rnum]] == m[rnum]

# <codecell>

rows_array[0]

# <codecell>

np.ma.clump_unmasked

# <codecell>

["".join(list(rows_array[0][s])).strip() for s in np.ma.clump_unmasked(np.ma.array(rows_array[0], mask =mask))]

# <headingcell level=1>

# Addendum:  creating column markers to read off column numbers

# <markdowncell>

# 
# 0...9
# a...i
# A...I
# 
# repeat...

# <codecell>

import string
from itertools import islice

upper = string.uppercase + "0"
lower = string.lowercase

def column_marker(start=0, stop=None):
    n = start
    while stop is None or n < stop:
        k = n % 10
        if k > 0:
            yield unicode(k)
        else:
            if n % 100 == 0:
                yield unicode(upper[(n % 1000) / 100 -1 ])
            elif n % 10 == 0 :
                yield unicode(lower[(n % 100) / 10  - 1])
        
        n += 1

# <codecell>

len(list(column_marker(0,12)))

# <codecell>

print "".join(column_marker(0,180))

# <markdowncell>

# <pre>
# 0123456789a123456789b123456789c123456789d123456789e123456789f123456789g123456789h123456789i123456789A123456789a123456789b123456789c123456789d123456789e123456789f123456789
# PST045212 Resident total population estimate (July 1) 2012                                                         ABS    0      313914040      576412   313914040  CENSUS
# PST045211 Resident total population estimate (July 1) 2011                                                         ABS    0      311587816          90   311587816  CENSUS
# PST040210 Resident total population, estimates base (April 1) 2010                                                 ABS    0      308747508          82   308747508  CENSUS
# PST120212 Resident total population, percent change - April 1, 2010 to July 1, 2012                                PCT    1            1.7        -0.2         5.1  CENSUS
# PST120211 Resident total population, percent change - April 1, 2010 to July 1, 2011                                PCT    1            0.9       -18.1        14.6  CENSUS
# POP010210 Resident population (April 1 - complete count) 2010                                                      ABS    0      308745538          82   308745538  CENSUS
# AGE135211 Resident population under 5 years, percent, 2011                                                         PCT    1            6.5         0.0        13.3  CENSUS
# A
# </pre>

# <markdowncell>

# Reading off the columns
# 
# * 0, 8
# * 10, 111
# * 115, 117
# * 122
# * 129, 137
# * 144, 149
# * 153, 161
# * 164, 169
# 
# [u'Data_Item', u'Item_Description', u'Unit', u'Decimal', u'US_Total', u'Minimum', u'Maximum', u'Source']

# <codecell>


