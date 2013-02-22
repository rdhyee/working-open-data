# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <headingcell level=1>

# Making http requests in Python

# <markdowncell>

# a refresher on http might be in order: http://mashupguide.net/1.0/html/ch06s04.xhtml#d0e10474

# <headingcell level=1>

# requests library

# <markdowncell>

# I like using requests even though there are several alternatives: http://lumberjaph.net/python/2012/02/17/HTTP_requests_with_python.html
# 
# 
# http://docs.python-requests.org/en/latest/
# 
# enpkg knows about requests:
# 
# > enpkg -s 
# 
# yields
# 
#     Name                   Versions           Note
#     ------------------------------------------------------------
#     requests               0.3.0-1            
#                            0.3.1-1            
#                            0.3.2-1            
#                            0.4.1-1            
#                            0.5.0-1            
#                            0.6.1-1            
#                            0.6.4-1            
#                            0.7.4-1            
#                            0.9.0-1            
#                            0.9.1-1            
#                            0.9.3-1            
#                            0.10.1-1           
# 
# 

# <headingcell level=1>

# geocoding

# <markdowncell>

# normally, I like to use geocoder.us as an example -- see my book http://mashupguide.net/1.0/html/ch13s06.xhtml#d0e21349  -- but there have been overuse by bad actors

# <codecell>

import requests
import json


# https://developers.google.com/maps/documentation/geocoding/
# get Google lat, long
url = "http://maps.googleapis.com/maps/api/geocode/json?address=1600+Amphitheatre+Parkway,+Mountain+View,+CA&sensor=false"

r = requests.get(url)

# <codecell>

r.status_code

# <codecell>

r.headers['content-type']

# <codecell>

r.text

# <codecell>

r.json()

# <codecell>

r.json()['results'][0]['geometry']['location']

# <headingcell level=1>

# lxml for a bit of scraping

# <codecell>

import requests
from lxml.html import parse
from StringIO import StringIO

ry_class_url = "http://osoc.berkeley.edu/OSOC/osoc?p_term=SP&p_deptname=INFO&p_instr=yee"
r = requests.get(ry_class_url)
doc = parse(StringIO(r.content)).getroot()

course_tts = doc.cssselect('table:nth-of-type(2) tt')

print course_tts[-1].text_content().replace("Avail Seats", "Avail_Seats").split(" ")[:-1]

# <codecell>


