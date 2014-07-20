# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <markdowncell>

# How to plot counties and shade them according with a specified color?
# 
# I forgot that this has been an [old question for me](http://blog.dataunbound.com/2009/09/03/plotting-data-for-counties-on-google-maps-part-i/).
# 
# 
# 

# <markdowncell>

# Where to get county shape files?
# 
# * A [UScounty shapefile is included in basemap version 1.0.6](https://github.com/matplotlib/basemap/commits/v1.0.6rel/lib/mpl_toolkits/basemap/data/UScounties.shp). Unfortunately, the latest version of basemap provided by enpkg is 1.0.2 (and I've not successfully been able to compile from source on a Mac).
# 
# * I think it's safe to copy the USCounties files over from version 1.0.6 to your basemap data directory, but I'd rather not add files to that directory.
# 
# * Alternative:  download files from US Census
# 
# http://www.census.gov/geo/www/tiger/tgrshp2012/tgrshp2012.html
# 
# ftp interface: ftp://ftp2.census.gov/geo/tiger/TIGER2012/COUNTY/ -> ftp://ftp2.census.gov/geo/tiger/TIGER2012/COUNTY/tl_2012_us_county.zip
# 
# I've not added these files to the working-open-data repo because I don't want large data files in the repo if possible.

# <codecell>

import numpy as np
import matplotlib.pyplot as plt
import warnings

with warnings.catch_warnings():
    warnings.simplefilter("ignore")

    from mpl_toolkits.basemap import Basemap

# <codecell>

# you can figure out where the data directory for basemap is

import os
import inspect
basemap_data_dir = os.path.join(os.path.dirname(inspect.getfile(Basemap)), "data")
print basemap_data_dir, os.path.exists(os.path.join(basemap_data_dir,"UScounties.shp"))

# <codecell>

!ls $basemap_data_dir

# <codecell>

# https://code.google.com/p/pyshp/
# pip install pyshp
import shapefile
 
# this is my git clone of https://github.com/matplotlib/basemap --> these files will be in the PiCloud basemap_data_dir
if os.path.exists(os.path.join(basemap_data_dir,"UScounties.shp")):
    shpf = shapefile.Reader(os.path.join(basemap_data_dir,"UScounties"))
else:
    # put in your path
    #shpf = shapefile.Reader("/Users/raymondyee/Dropbox/WwoD13/tl_2012_us_county")
    shpf = shapefile.Reader("/Users/raymondyee/C/src/basemap/lib/mpl_toolkits/basemap/data/UScounties")

shapes = shpf.shapes()
records = shpf.records()

# <codecell>

shpf.fields

# <codecell>

zip([f[0] for f in shpf.fields[1:]], records[0])

# <codecell>

# just CA

from itertools import islice, izip
len([r for r in islice(records,None) if r[0] == '06'])

# <codecell>

def zip_filter_by_state(records, shapes, included_states=None):
    # by default, no filtering
    # included_states is a list of states fips prefixes
    for (record, state) in izip(records, shapes):
        if record[0] in included_states:
            yield (record, state) 
    

# <codecell>

list(zip_filter_by_state(records, shapes, ['06']))

# <codecell>

len(shapes)

# <codecell>

# http://www.geophysique.be/2013/02/12/matplotlib-basemap-tutorial-10-shapefiles-unleached-continued/

#
# BaseMap example by geophysique.be
# tutorial 10
 
import os
import inspect
import numpy as np
import matplotlib.pyplot as plt
from itertools import islice, izip
from mpl_toolkits.basemap import Basemap
 
### PARAMETERS FOR MATPLOTLIB :
import matplotlib as mpl
mpl.rcParams['font.size'] = 10.
mpl.rcParams['font.family'] = 'Comic Sans MS'
mpl.rcParams['axes.labelsize'] = 8.
mpl.rcParams['xtick.labelsize'] = 6.
mpl.rcParams['ytick.labelsize'] = 6.
 
fig = plt.figure(figsize=(11.7,8.3))
#Custom adjust of the subplots
plt.subplots_adjust(left=0.05,right=0.95,top=0.90,bottom=0.05,wspace=0.15,hspace=0.05)
ax = plt.subplot(111)
#Let's create a basemap of USA
x1 = -180.
x2 = -62.
y1 = 18.
y2 = 68.
 
m = Basemap(resolution='i',projection='merc', llcrnrlat=y1,urcrnrlat=y2,llcrnrlon=x1,urcrnrlon=x2,lat_ts=(y1+y2)/2)
m.drawcountries(linewidth=0.5)
m.drawcoastlines(linewidth=0.5)
m.drawparallels(np.arange(y1,y2,2.),labels=[1,0,0,0],color='black',dashes=[1,0],labelstyle='+/-',linewidth=0.2) # draw parallels
m.drawmeridians(np.arange(x1,x2,2.),labels=[0,0,0,1],color='black',dashes=[1,0],labelstyle='+/-',linewidth=0.2) # draw meridians
 
    
def zip_filter_by_state(records, shapes, included_states=None):
    # by default, no filtering
    # included_states is a list of states fips prefixes
    for (record, state) in izip(records, shapes):
        if record[0] in included_states:
            yield (record, state) 
    
    
from matplotlib.collections import LineCollection
from matplotlib import cm
import shapefile 

basemap_data_dir = os.path.join(os.path.dirname(inspect.getfile(Basemap)), "data")

# this is my git clone of https://github.com/matplotlib/basemap --> these files will be in the PiCloud basemap_data_dir
if os.path.exists(os.path.join(basemap_data_dir,"UScounties.shp")):
    shpf = shapefile.Reader(os.path.join(basemap_data_dir,"UScounties"))
else:
    # put in your path
    #shpf = shapefile.Reader("/Users/raymondyee/Dropbox/WwoD13/tl_2012_us_county")
    shpf = shapefile.Reader("/Users/raymondyee/C/src/basemap/lib/mpl_toolkits/basemap/data/UScounties")

shapes = shpf.shapes()
records = shpf.records()
 
# show only CA and AK (for example)
for record, shape in zip_filter_by_state(records, shapes, ['06', '02']):
    lons,lats = zip(*shape.points)
    data = np.array(m(lons, lats)).T
 
    if len(shape.parts) == 1:
        segs = [data,]
    else:
        segs = []
        for i in range(1,len(shape.parts)):
            index = shape.parts[i-1]
            index2 = shape.parts[i]
            segs.append(data[index:index2])
        segs.append(data[index2:])
 
    lines = LineCollection(segs,antialiaseds=(1,))
    lines.set_facecolors(cm.jet(np.random.rand(1)))
    lines.set_edgecolors('k')
    lines.set_linewidth(0.1)
    ax.add_collection(lines)
 
plt.savefig('tutorial10.png',dpi=300)
plt.show()

# <codecell>


