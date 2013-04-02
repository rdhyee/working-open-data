# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <markdowncell>

# Working with Open Data Midterm (March 19, 2013)
# 
# *There are **84** points in this exam, but the test will be scored out of a base total of **60 points**.*
# 
# Name: ______________________________________
# 
# Date: ______________________________________
# 
# 

# <headingcell level=1>

# 1. Open data and the census (Total: 7)

# <markdowncell>

# **1a.**  <span style="font-weight:bold; color:red">[7]</span>  What is **open data**?  Use the US Census data set, specifically the Census Quickfacts (<http://quickfacts.census.gov/qfd/download_data.html>) that we've been studying in this course, to illustrate your definition of open data.  

# <markdowncell>

# * A piece of content or data is open if anyone is free to use, reuse, and redistribute it — subject only, at most, to the requirement to attribute and/or share-alike. (3)
# 
# * US Census data is free of copyright as a work of the US federal government and is free of charge. (2)
# 
# * some illustration of how census data can be used (2)

# <codecell>
















# <headingcell level=1>

# 2. CourtListener (Total: 7)

# <markdowncell>

# **2a.** <span style="font-weight:bold; color:red">[7]</span>  What problems is http://www.courtlistener.com/ trying to solve?   Why does CourtListener involve web scraping? 

# <markdowncell>

# * 4 for description of CourtListener, what it aggregates, that it's an alert service, offers bulk downloads, etc
# * 3 for what scraping is, lack of standards around how court data can be presented in structured form, APIs for how to access court cases, or how alerts done.

# <codecell>




















# <markdowncell>

# 
# 
# 
# 
# 
# 
# 
# 
# 
# 
# 

# <headingcell level=1>

# 3. Project Questions (Total: 14)

# <markdowncell>

# **3a.** <span style="font-weight:bold; color:red">[2]</span>  In a sentence or two, describe what are you aiming to accomplish in your project.

# <codecell>









# <markdowncell>

# **3b.** <span style="font-weight:bold; color:red">[8]</span>  What open data set are you using in your project?  How is that data open?

# <codecell>

















# <markdowncell>

# **3c.** <span style="font-weight:bold; color:red">[4]</span> What is an immediate next step in your project?

# <codecell>





















# <headingcell level=1>

# 4. Verifying population totals in Census (Total: 20)

# <markdowncell>

# Consider the following code to calculate the population of the US, state-like entities, and county-like entities.
# 

# <codecell>

import pandas as pd
from pandas import Series, DataFrame

from itertools import islice

import datetime

from itertools import islice
import codecs
import re
import csv

import os

if os.getcwd() == '/home/picloud/notebook':
    ON_PICLOUD = True
    DATA_DIR = '/home/picloud/working-open-data/data'
    PYDATA_DIR = '/home/picloud/pydata-book/'
else:
    ON_PICLOUD = False
    DATA_DIR = os.path.join(os.pardir, "data")
    PYDATA_DIR = os.path.join(os.pardir, "pydata-book")
    
dataset_fname = os.path.join (DATA_DIR, "census/DataSet.txt")
datadict_fname = os.path.join (DATA_DIR, "census/DataDict.txt")
fips_fname = os.path.join (DATA_DIR, "census/FIPS_CountyName.txt")

assert os.path.exists(DATA_DIR)
assert os.path.exists(PYDATA_DIR)
assert os.path.exists(dataset_fname)
assert os.path.exists(datadict_fname)
assert os.path.exists(fips_fname)


# read in fips code
fips_file = codecs.open(fips_fname, encoding='iso-8859-1')

fips = dict()
for row in islice(fips_file, None):
    fips[row[:5]] = row[6:-1]
    

# read in data set
ds_file = codecs.open(dataset_fname, encoding='iso-8859-1')
reader = csv.DictReader(ds_file)
dataset = dict([(row["fips"], row) for row in islice(reader, None)])
    
states_fips = sorted([k for k in fips.keys() if k[-3:] == '000' and k != '00000'])

# <markdowncell>

# And look at the following outputs to remind you of the content of the data set:

# <codecell>

!head $fips_fname

# <codecell>

dataset["00000"]["POP010210"]

# <codecell>

for f in states_fips[:5]:
    print f, fips[f]

# <codecell>

list(islice(sorted(dataset.keys()),5))

# <codecell>

fips['06000']

# <headingcell level=2>

# Questions for Section 4

# <codecell>

# number of counties in CA

from collections import Counter
print Counter([k[0:2] for k in dataset.keys() if k[2:5] != '000'])['06']

# <markdowncell>

# **4a.** <span style="font-weight:bold; color:red">[6]</span>  Explain how the following code (which produces `58`) shows that the number of counties in California is 58:
# 
#     from collections import Counter
#     print Counter([k[0:2] for k in dataset.keys() if k[2:5] != '000'])['06']
# 
# Include in your explaination:
# 
# * what `Counter` does
# * the significance of `k[0:2]`
# * why do we have `k[2:5] != '000'`
# * why `['06']` is part of the code

# <markdowncell>

# * list comprehension of state prefixes by filtering on counties
# * Counter then takes tallies those state prefixes
# * state prefix from 1st 2 characters of fips code
# * counties don't end in '000'
# * California prefix is 06
# * what Counter does: Counter takes iterable and creats a count value for all values in iterable -- these values become keys

# <codecell>


















# <markdowncell>

# **4b.** <span style="font-weight:bold; color:red">[4]</span>  Explain what the following piece of code calculates (and how), and what the answer is:
# 
#     len([k for k in dataset.keys() if k[2:5] == '000' and k != '00000'])

# <markdowncell>

# * 2 for answer
# * 1 for explaining "grammar" of the statement -- e.g., `len` gives number of elements
# * 1 for semantics -- e.g., 50 states + DC = 51; exclude USA ('00000'); include state like entites (ends in '000'))

# <codecell>















# <markdowncell>

# **4c.** <span style="font-weight:bold; color:red">[5]</span> What is the answer to following?
# 
#     sum([int(dataset[k]["POP010210"]) for k in dataset.keys() if k[2:5] == '000' and k != '00000']) 
# 
# 
# Explain how you came up with the answer.

# <markdowncell>

# * quote the exact pop of USA
# * get states by looking for '000' ending but exclude US ('00000')
# * dataset[k]['POP010210'] holds census pop for fips code k 
# * need int() coercion
# * sum -- to add up all in list

# <codecell>














# <markdowncell>

# **4d.** <span style="font-weight:bold; color:red">[5]</span> What is the answer to following?
# 
#     sum([int(dataset[k]["POP010210"]) for k in dataset.keys() if k[2:5] != '000'])
# 
# Explain how you came up with the answer.

# <markdowncell>

# * quote the exact pop of USA
# * get counties by looking for '000' ending but exclude US ('00000')
# * dataset[k]['POP010210'] holds census pop for fips code k 
# * need int() coercion
# * sum -- to add up all in list
# * ok to say that logic of 4d is same as 4c except county -- no need to write it all out again

# <codecell>











# <headingcell level=1>

# 5. Slice notation (Total: 7)

# <markdowncell>

# Consider the following code using slice notation:

# <codecell>

import string
alphabet = string.lowercase

alphabet

print "alphabet:", alphabet
print "alphabet[0]:", alphabet[0]
print "alphabet[-1], alphabet[0:5], alphabet[-2:]:", alphabet[-1], alphabet[0:5], alphabet[-2:]

# <headingcell level=2>

# Calculate the following:

# <markdowncell>

# **5a.** <span style="font-weight:bold; color:red">[1]</span>  `alphabet[5]`

# <codecell>

alphabet[5]

# <codecell>




# <markdowncell>

# **5b.** <span style="font-weight:bold; color:red">[1]</span>  `alphabet[0:3]`

# <codecell>

alphabet[0:3]

# <codecell>




# <markdowncell>

# **5c.** <span style="font-weight:bold; color:red">[2]</span>  `alphabet[1:4:2]`

# <codecell>

alphabet[1:4:2]

# <codecell>




# <markdowncell>

# **5d.** <span style="font-weight:bold; color:red">[1]</span> `alphabet[-6:]`

# <codecell>

alphabet[-6:]

# <codecell>




# <markdowncell>

# **5e.** <span style="font-weight:bold; color:red">[2]</span>  `alphabet[-1:-3:-1]`

# <codecell>

alphabet[-1:-3:-1]

# <codecell>





# <headingcell level=1>

# 6. ndarray (Total: 3)

# <codecell>

a = array([0,1,2,3])

# <codecell>

a + 5

# <markdowncell>

# **6a.** <span style="font-weight:bold; color:red">[3]</span> Given that 
# 
#     a = array([0,1,2,3])
# 
# and that 
# 
#     a + 5 
# 
# is:
# 
#     array([5, 6, 7, 8])
# 
# what is:
# 
#     sum(2*a)
# 
# 

# <codecell>

sum(2*a)

# <codecell>














# <headingcell level=1>

# 7. Chemical elements DataFrame (Total: 18)

# <markdowncell>

# Consider the following `DataFrame` holding information about the lightest chemical elements

# <codecell>

# round off atomic weight

elements = DataFrame([{'number': 1, 'name': 'hydrogen', 'weight':1}, 
                      {'number': 2, 'name': 'helium', 'weight':4},
                      {'number': 3, 'name': 'lithium', 'weight':7},
                      {'number': 4, 'name': 'beryllium', 'weight':9},
                      {'number': 5, 'name': 'boron', 'weight':11},
                      {'number': 6, 'name': 'carbon', 'weight':12},
                     ], index= ['H', 'He', 'Li', 'Be', 'B', 'C'])

# add group information

elements['group'] = Series([1, 18, 1, 2, 13, 14], index = ['H', 'He', 'Li', 'Be', 'B', 'C'])

elements







# <headingcell level=2>

# Calculate the following  (showing how you arrive at your answer)

# <markdowncell>

# **7a.** <span style="font-weight:bold; color:red">[1]</span> 

# <codecell>

len(elements.index)

# <codecell>



# <markdowncell>

# **7b.** <span style="font-weight:bold; color:red">[4]</span> 

# <codecell>

elements[elements.number > 4]["weight"].sum()

# <codecell>









# <markdowncell>

# **7c.** <span style="font-weight:bold; color:red">[4]</span> 

# <codecell>

set(elements[elements['group'] == 1].name)

# <codecell>









# <markdowncell>

# **7d.** <span style="font-weight:bold; color:red">[4]</span> 

# <codecell>

elements.sort_index(by='weight')['number'][::-1][:2].sum()

# <codecell>












# <headingcell level=2>

# Now we add comments to DataFrame

# <codecell>

comments = Series(['first and most common element', 'the C in organic'], index=['H', 'C'])

# <codecell>

elements['comments'] = comments
elements

# <headingcell level=2>

# Calculate the following, again showing how you arrive at your answer

# <markdowncell>

# **7e.** <span style="font-weight:bold; color:red">[1]</span> 

# <codecell>

elements.comments.dropna().count()

# <codecell>





# <markdowncell>

# **7f.** <span style="font-weight:bold; color:red">[4]</span> 

# <codecell>

"".join(elements.comments.dropna().apply(lambda x: x[0]).values)

# <codecell>










# <headingcell level=3>

# Hints for Question 7f

# <codecell>

"".join(['a','b'])

# <codecell>

elements.number.apply(lambda x: 2*x)

# <codecell>

"".join(elements.number.apply(lambda x: str(2*x)).values)

# <headingcell level=1>

# 8. Matching the capitals to latitude, longitude pairs (Total: 4)

# <markdowncell>

# <img src="https://www.evernote.com/shard/s1/sh/b5dd80cb-740d-4aa2-a2a7-151fd0e3119b/77a2a008cbee7050a323c5302075ab1b/res/b777ee6b-b293-4e2c-b4e8-2313e6db7af0/Google_Maps-20130317-171357.jpg.jpg?resizeSmall&width=500">

# <markdowncell>

# **8a.** <span style="font-weight:bold; color:red">[4]</span>  Match the following capital cities to their respective latitude, longitudes -- to each number, match a letter:
# 
# 1.  Ottawa, Canada:          ____________
# 2.  Moscow, Russia:          ____________
# 3.  Manila, Philippines:     ____________
# 4.  Buenos Aires, Argentina: ____________
# 
# Lat/long:
# 
#     A (14.583333, 120.966667)
#     B (45.420833, -75.69)
#     C (-34.603333, -58.381667)
#     D (55.75, 37.616667)

# <markdowncell>

# B, D, A, C

# <headingcell level=1>

# 9. datetime (Total: 4)

# <codecell>

import datetime

# <markdowncell>

# **9a.** <span style="font-weight:bold; color:red">[2]</span> What is
# 
#     

# <codecell>

(datetime.datetime.now() + datetime.timedelta(days=20)).month

# <markdowncell>

# 4

# <codecell>






# <markdowncell>

# **9b.** <span style="font-weight:bold; color:red">[2]</span>  

# <markdowncell>

# What does the following code print:
# 
#     dt = datetime.datetime.fromtimestamp(24*60*60*5) - datetime.datetime.fromtimestamp(0)
#     print dt.days

# <markdowncell>

# 5

# <codecell>







