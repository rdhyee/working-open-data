# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <headingcell level=1>

# Goals

# <markdowncell>

# We will be working with [Freebase][http://dev.freebase.com] and [OpenRefine](http://openrefine.org/) throughout the semester.  Today, I wanted to get us set up with using the API -- the goal today is simply for all of you to go get a Google API key and configure 

# <markdowncell>

# Follow instructions at
# 
# http://wiki.freebase.com/wiki/Freebase_API#Getting_Started
# 
# to get a key.  You may need to go to the Services section at https://code.google.com/apis/console/b/0/ to make sure Freebase access is turned on:
# 
# <img src="https://www.evernote.com/shard/s1/sh/0c4fb5bf-d3af-4ab6-a249-e6ee92d93ca6/5534f2603dd54ba2d0bbb5a3bbc36cc5/res/6c448c96-5821-4ef0-be80-1eab40825351/Google_APIs_Console-20130214-093024.jpg.jpg?resizeSmall&width=832" />
# 
# <img src="https://www.evernote.com/shard/s1/sh/a19bdb08-69ae-4902-909e-d521627ca16f/f9b32ea595d0206a0a567afe2e19af23/res/f272e2ce-f8d2-41a5-8bad-21d8c3a14f3b/Google_APIs_Console-20130214-093415.jpg.jpg?resizeSmall&width=832" />
# 
# 
# Then go to the API Access screen and the Create New Browser Key button on bottom of page to get a key.
# 
# Make a CREDENTIALS.py  in the same directory as your IPython notebooks to hold this key:
# 
# FREEBASE_KEY = '[INSERT_YOUR_KEY]'
# 
# You need to confKey for browser apps (with referers)

# <headingcell level=1>

# Sample Code to pull up list of planets

# <codecell>

# https://dev.freebase.com/astronomy/planet?instances
# http://wiki.freebase.com/wiki/Google_API_Client_Libraries#Python

from apiclient import discovery
from apiclient import model
import json
from CREDENTIALS import FREEBASE_KEY

DEVELOPER_KEY = FREEBASE_KEY

model.JsonModel.alt_param = ""
freebase = discovery.build('freebase', 'v1', developerKey=DEVELOPER_KEY)
query = [{'id': None, 'name': None, 'type': '/astronomy/planet'}]

response = json.loads(freebase.mqlread(query=json.dumps(query)).execute())
planets = []

for planet in response['result']:
	print planet['name']
    
	planets.append(planet['name'])
    
assert planets == [u'Earth',
 u'Venus',
 u'Mars',
 u'Mercury',
 u'Jupiter',
 u'Neptune',
 u'Saturn',
 u'Uranus']

# <headingcell level=1>

# Pulling up all current US State Governors, their party affiliations, and Wikipedia page ids

# <codecell>

# http://wiki.freebase.com/wiki/Google_API_Client_Libraries#Python

from itertools import islice

from apiclient import discovery
from apiclient import model
import json
from CREDENTIALS import FREEBASE_KEY

from pandas import DataFrame, Series

DEVELOPER_KEY = FREEBASE_KEY

model.JsonModel.alt_param = ""
freebase = discovery.build('freebase', 'v1', developerKey=DEVELOPER_KEY)

query_json = """[{
  "id": null,
  "wiki_en:key": [{
    "/type/key/namespace": "/wikipedia/en_id",
    "value":         null,
    "optional":      true
  }],
  "/location/administrative_division/fips_10_4_region_code": null,
  "/location/administrative_division/first_level_division_of": "United States of America",
  "type": "/government/governmental_jurisdiction",
  "governing_officials": [{
    "type":        null,
    "office_holder": {
      "id":   null,
      "en:name": null,
      "type": "/government/politician",
      "party": [{
        "party": null
      }]
    },
    "basic_title": "Governor",
    "from":  null,
    "to": {
      "optional": "forbidden",
      "value":    null
    }
  }]
}]""".replace("\n", " ")


query = json.loads(query_json)

response = json.loads(freebase.mqlread(query=json.dumps(query)).execute())

results=list()

for result in islice(response['result'], None):
    #print result
    results.append( {'fips': result['/location/administrative_division/fips_10_4_region_code'], 
           'state': result['id'],
           'name': result['governing_officials'][0]['office_holder']['en:name'], 
           'party': [p['party'] for p in result['governing_officials'][0]['office_holder']['party']],
           'en_wikipedia_key': [k["value"] for k in result["wiki_en:key"]]
           })
    
governors = DataFrame(results)
governors[:5]

# <codecell>

# which ones are Republicans (or have been Republican)

governors[governors["party"].apply(lambda x: 'Republican Party' in x)]

# <headingcell level=1>

# Rewriting sample code to provide a generator

# <codecell>

# state centroids
# http://tinyurl.com/cjuy6k3

from itertools import islice

from apiclient import discovery
from apiclient import model
import json
from CREDENTIALS import FREEBASE_KEY

from pandas import DataFrame, Series

DEVELOPER_KEY = FREEBASE_KEY

model.JsonModel.alt_param = ""
freebase = discovery.build('freebase', 'v1', developerKey=DEVELOPER_KEY)

query_json = """
[{
  "id": null,
  "name": null,
  "/location/administrative_division/fips_10_4_region_code": [],
  "/location/administrative_division/first_level_division_of": "United States of America",
  "/location/location/geolocation": {
    "latitude": null,
    "longitude": null
  }
}]""".replace("\n", " ")

query = json.loads(query_json)

response = json.loads(freebase.mqlread(query=json.dumps(query)).execute())

results = list()

for result in islice(response['result'], None):
    results.append( {'id': result['id'],
                     'name': result['name'],
                     'latitude': float(result['/location/location/geolocation']['latitude']),
                     'longitude': float(result['/location/location/geolocation']['longitude']),
                     'fips': result['/location/administrative_division/fips_10_4_region_code'],
                     } )
    
states = DataFrame(results)
plt.scatter(states["longitude"], states["latitude"])
    

# <codecell>

# handling cursors
# http://wiki.freebase.com/wiki/MQL_Read_Service#cursor
# https://developers.google.com/freebase/v1/mql-overview#looping-through-cursor-results

from itertools import islice
from apiclient import discovery
from apiclient import model
import json
from pandas import DataFrame, Series

from CREDENTIALS import FREEBASE_KEY
DEVELOPER_KEY = FREEBASE_KEY


model.JsonModel.alt_param = ""
freebase = discovery.build('freebase', 'v1', developerKey=DEVELOPER_KEY)

query_json = """
[{
  "id": null,
  "name": null,
  "wiki_en:key": [{
    "/type/key/namespace": "/wikipedia/en_id",
    "value":         null,
    "optional":      true
  }],
  "/location/administrative_division/fips_10_4_region_code": [],
  "/location/administrative_division/second_level_division_of": "United States of America",
  "/location/location/geolocation": {
    "latitude": null,
    "longitude": null
  }
}]""".replace("\n", " ")

query = json.loads(query_json)

    
def freebase_query(query, cursor=""):
    
    while True:
        response = json.loads(freebase.mqlread(query=json.dumps(query), cursor=cursor).execute())
        for item in response['result']:
            yield item
            
        cursor = response.get("cursor")
        if not cursor:
            break


results = []

for (i,result) in enumerate(islice(freebase_query(query), None)):
    print i,
    results.append( {'id': result['id'],
              'name': result['name'],
              'latitude': float(result['/location/location/geolocation']['latitude']),
              'longitude': float(result['/location/location/geolocation']['longitude']),
              'fips': result['/location/administrative_division/fips_10_4_region_code'],
              'wikipedia_en_id': [k['value'] for k in result['wiki_en:key']]
             })
    
counties = DataFrame(results)

# write out a CSV
# http://pandas.pydata.org/pandas-docs/dev/io.html#writing-to-csv-format

import codecs
import os

outfile_path = "/Users/raymondyee/D/Document/Working_with_Open_Data/working-open-data/data/freebase/counties.csv"
outfile = codecs.open(outfile_path, mode="wb", encoding='utf-8')

counties.to_csv(outfile)

outfile.close()

# <codecell>

counties

# <codecell>

counties_plot = plt.scatter(counties["longitude"], counties["latitude"],  s=1, lw = 0.2, facecolor="blue")

# <codecell>


