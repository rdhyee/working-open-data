# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <headingcell level=1>

# Overview

# <markdowncell>

# intro to understanding timestamps and datetime in context of `PfDA`
# 
# * [datetime](http://docs.python.org/2/library/datetime.html) standard library -- nicely explained in [PyMOTW](http://pymotw.com/2/datetime/index.html)
# * [time](http://docs.python.org/2/library/time.html) standard library
# 
# Also two modules available in EPD among other places:
# 
# * [pytz](http://pytz.sourceforge.net/)
# * [python_dateutil](ttp://labix.org/python-dateutil)
# 
# Wonderful tutorial on converting among various time formats: [Date and Time Representation in Python](http://www.seehuhn.de/pages/pdate)

# <codecell>

# http://docs.python.org/2/library/datetime.html
# http://docs.python.org/2/library/time.html

import datetime
import time

import pytz
import dateutil

# <headingcell level=1>

# datetime.datetime.now and utcnow

# <markdowncell>

# Basic task:  get current local datetime -- notice no timezone info -- datetime.now() is "timezone naive"

# <codecell>

t =  datetime.datetime.now()

print t
print 'hour  :', t.hour
print 'minute:', t.minute
print 'second:', t.second
print 'microsecond:', t.microsecond
print 'tzinfo:', t.tzinfo

# <markdowncell>

# Similarly -- can get UTC  http://en.wikipedia.org/wiki/Coordinated_Universal_Time

# <codecell>

t = datetime.datetime.utcnow()

print t
print 'hour  :', t.hour
print 'minute:', t.minute
print 'second:', t.second
print 'microsecond:', t.microsecond
print 'tzinfo:', t.tzinfo

# <headingcell level=1>

# time zones

# <markdowncell>

# I've used pytz for time zones...I think dateutil has similar functionality but not sure

# <codecell>

pytz.utc

# <codecell>

# I'm assuming for our purposes here that we are in Pacific time
pacific_tz = pytz.timezone('US/Pacific')

# <codecell>

# make tz-aware datetimes

t = pacific_tz.localize(datetime.datetime.now())
t_utc = pytz.utc.localize(datetime.datetime.utcnow())

print t
print 'hour  :', t.hour
print 'minute:', t.minute
print 'second:', t.second
print 'microsecond:', t.microsecond
print 'tzinfo:', t.tzinfo

# <codecell>

# example of using astimezone to represent in different tz
t.astimezone(pytz.utc)

# <codecell>

t, t_utc, t_utc-t, (t_utc-t).total_seconds()

# <headingcell level=1>

# time module

# <codecell>

# http://pymotw.com/2/time/index.html

time.ctime()

# <codecell>

# number of seconds since Jan 1, 1970 UTC
# http://www.epochconverter.com/
time.time()

# <codecell>

# use of fromtimestamp to convert Unix Epoch time to datetime.datetime
datetime.datetime.fromtimestamp(time.time())

# <codecell>

(datetime.datetime.now() - datetime.datetime.fromtimestamp(time.time())).total_seconds()

# <codecell>

datetime.datetime(1970,1,1,0,0,0)

# <codecell>

datetime.datetime.fromtimestamp(0.0)

# <codecell>

# show that if we are Pacific time as local time -- that 0 epoch time UTC
pacific_tz.localize(datetime.datetime.fromtimestamp(0.0)).astimezone(pytz.utc)

# <codecell>

# http://www.seehuhn.de/pages/pdate
# coverting datetime to epoch time
t=datetime.datetime.now()
timestamp_now = time.mktime(t.timetuple())+1e-6*t.microsecond
pacific_tz.localize(datetime.datetime.fromtimestamp(timestamp_now))

# <headingcell level=1>

# Any need to hardwire Pacific Time?  No...use tzlocal perhaps

# <codecell>

import dateutil

# <codecell>

# does tzlocal work?

t = datetime.datetime.now(dateutil.tz.tzlocal())
t.tzname()

# <codecell>

t.astimezone(pytz.utc)

