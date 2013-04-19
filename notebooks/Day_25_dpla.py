# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <markdowncell>

# launch of dp.la API v2: 
# https://cyber.law.harvard.edu/lists/arc/dpla-tech/2013-04/msg00004.html
# 
# Need a key, which you can get, using [incantation from Tom Morris](https://cyber.law.harvard.edu/lists/arc/dpla-tech/2013-04/msg00007.html):
# 
#     curl -v -XPOST http://api.dp.la/v2/api_key/you@your_email.com
# 
# As Tom wrote:  "If you use Gmail, check your spam folder. The key is sent immediately."

# <markdowncell>

# Europeana API: http://pro.europeana.eu/api

# <codecell>

# Goal:  feed a bunch of search terms to try to get at some collections

# API doc: https://github.com/dpla/platform/
# test data sources: http://dp.la/wiki/Platform_test_data_sources

import requests
import json
import urllib
from itertools import islice

from CREDENTIALS import DPLA_KEY

# http://api.dp.la/v2/items?api_key=YOUR_API_KEY

# Retrieve an item by ID
# http://api.dp.la/v2/items/a4e2346032cae75b0832abe064c14bcb

# Retrieve multiple items by ID
# http://api.dp.la/v1/items/a4e2346032cae75b0832abe0644e9b26,a4e2346032cae75b0832abe064c14bcb


def dpla_query(**kw_input):
    
    kwargs = {"page_size": 20, "page": 1, "sort_order":"asc", "api_key":DPLA_KEY}
    
    # fudgy -- allow an extra parameter to allow for ones that can fit kw_input -- e.g., spatial.coordinates
    extras = kw_input.pop('extras',{})
    kw_input.update(extras)
    
    kwargs.update(kw_input)
    kwargs = dict([(k,v) for (k,v) in kwargs.items() if v is not None])
    
    # asc vs desc
    
    # available text search fields
    text_search_fields = ("title", "description", "dplaContributor", "creator", "type", "publisher", "format", "rights", "contributor", "spatial")
    expected_doc_fields = ['title','description', 'creator', 'type', 'publisher', 'format', 'rights', 'contributor', 'created', 'spatial', 'temporal', 'source']
    
    # temporal fields
    # http://api.dp.la/v1/items?temporal.after=1963-11-01&temporal.before=1963-11-30
    
    # location available...not implemented here
    more_items = True
    
   # content["count"], content["start"], content["limit"]
    
    while more_items:
        
        r = requests.get("http://api.dp.la/v2/items?" + urllib.urlencode(kwargs))
        content = json.loads(r.content)
        
        if len(content.get("docs", [])):
            for doc in content["docs"]:
                yield (doc, content["count"])
            if kwargs['sort_order'] == 'desc':
                kwargs['page'] -= 1
            else:
                kwargs['page'] += 1
        else:
            more_items = False


# search terms to feed in 

SEARCH_TERMS = ["Bach", "tree", "horse", "cow", "Gore"]

# collections 
collections = set()

for term in islice(SEARCH_TERMS,1):
    results = list(islice(dpla_query(q=term),100)) 
            
    for (i, (doc, count)) in enumerate(results):
        collections.add(doc.get('isPartOf', {'title':None}).get('title'))
    
print len(collections)

# for each collection let's figure out the number of items in the collection

from IPython.display import HTML
from jinja2 import Template

num_items = []

for (i, collection) in enumerate(sorted(collections)):
    if collection is not None:
        size_collection = list(islice(dpla_query(isPartOf=collection),1))[0][1] if collection is not None else 0
        url = "http://api.dp.la/v1/items?" + urllib.urlencode({'isPartOf': collection})
        num_items.append((collection, size_collection, url))
    else:
        num_items.append((None, 0, ""))
    
TABLE_TEMPLATE = """<table>
 <tr>
   <th>Collection</th>
   <th>Number of items</th>
   <th>API</th>
 </tr>
 {% for num_item in num_items %}
 <tr>
  <td>{{num_item.0}}</td>
  <td>{{num_item.1}}</td>
  <td><a href="{{num_item.2}}">{{num_item.2}}</a></td>
{% endfor %}
 </tr>
"""
    
template = Template(TABLE_TEMPLATE)
HTML(template.render(num_items=num_items))  

# <codecell>

r = dpla_query(q='Bach')

# <codecell>

r0 = list(islice(r,10))

# <codecell>

r0

# <codecell>


