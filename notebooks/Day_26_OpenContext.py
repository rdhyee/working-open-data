# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <markdowncell>

# # A quick jump into the API of opencontext.org
# 
# Let's use a specific project to focus on:
# 
# * <http://opencontext.org/sets/?proj=Asian+Stoneware+Jars>
# * <http://opencontext.org/lightbox/?proj=Asian+Stoneware+Jars>
# 
# 
# The API documentation: <http://opencontext.org/about/services>

# <codecell>

# using an example in the API documentation to confirm that we can get json representation from API

import requests
json_url = "http://opencontext.org/sets/Palestinian+Authority/Tell+en-Nasbeh/.json?proj=Bade+Museum"

r = requests.get(json_url)

# what are the top level keys of response?
r.json().keys()

# <codecell>

# Now let's apply same logic to the Asian Stoneware Jars project

json_url = "http://opencontext.org/sets/.json?proj=Asian+Stoneware+Jars"

request = requests.get(json_url)
request_json = request.json()

results= request_json['results']

# <codecell>

request_json.keys()

# <codecell>

# number of results matches what is on human UI
request_json['numFound']

# <codecell>

# we get back the first page of 10
len(results)

# <codecell>

results[0]

# <codecell>

# list the URLs for the thumbnails
[result.get('thumbIcon') for result in results]

# <codecell>

# do a quick display

from IPython.display import HTML
from jinja2 import Template


IMAGES_TEMPLATE = """
 {% for item in items %}
<img title="{{item.label}}" src="{{item.thumbIcon}}"/>
 {% endfor %}
"""
    
template = Template(IMAGES_TEMPLATE)
HTML(template.render(items=results)) 

# <codecell>


