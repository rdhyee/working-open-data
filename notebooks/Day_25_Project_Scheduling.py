# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

import random
random.seed()
# random.getstate()

# <codecell>

projects = ['Health Care Treatment or Prevention?  An Environmental Outlook',
'The League of Champions',
'World Bank Data : Projects and Operations',
'All about TED',
'Education First',
'Dr. Book - Linking a Book to Open Data Sources',
'Book Hunters',
'Stock Performance of Product Releases']

# <codecell>

# every time you run this, you get a new permutation
# I did it a few time and stopped at random to get the following permutation

random.shuffle(projects)
projects

# <codecell>

print "(Day 27) Tuesday April 30"
for (i, p) in enumerate(projects[0:4]):
    print i+1, p
print 
print "(Day 28) Thursday May 2"
for (i, p) in enumerate(projects[4:8]):
    print i+1, p

