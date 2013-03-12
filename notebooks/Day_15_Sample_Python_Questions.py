# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

import pandas as pd
from pandas import Series, DataFrame

from itertools import islice

import datetime
import time
import pytz

# <codecell>

s0 = "Open Data"
len(s0), s0[::-1], s0[2]

# <codecell>

# something simple to start
datetime.datetime.now().month

# <codecell>

# tests whether you know the basics of datetime, what fromtimestap does, and notion of timedelta

dt = datetime.datetime.fromtimestamp(86400) - datetime.datetime.fromtimestamp(0)
dt.total_seconds(), dt.days

# <codecell>

pytz.timezone('US/Pacific').localize(datetime.datetime.fromtimestamp(0)).astimezone(pytz.utc)

# <codecell>

def triangle():
    f = 0
    n = 1
    while True:
        f += n
        yield f
        n += 1

# <codecell>

# hint list(islice([0,1,2,3,4], 2))  is [0,1]

f = triangle()
list(islice(f,4))

# <codecell>

s  = Series(arange(3), index = ['a','b','c'])
s['b']

# <codecell>

s.order()[::-1][0]

# <codecell>

df = DataFrame([{'name':'UC Berkeley', 'city':'Berkeley', 'state':'CA'}, {'name':'MIT', 'city':'Cambridge', 'state':'MA'},
                {'name':'Stanford', 'city':'Stanford', 'state':'CA'}, {'name':'Harvard', 'city':'Cambridge', 'state':'MA'}])
sum(df[df.state == 'CA'].name.str.len())

# put into words what we're trying to calculate and give  the answer

