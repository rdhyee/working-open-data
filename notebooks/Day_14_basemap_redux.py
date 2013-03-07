# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <headingcell level=1>

# BaseMap

# <markdowncell>

# Working through http://matplotlib.org/basemap/
# 
# * http://en.wikipedia.org/wiki/Map_projection
# * http://matplotlib.org/basemap/users/mapsetup.html

# <codecell>

# http://matplotlib.org/basemap/users/examples.html

from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import numpy as np

# set up orthographic map projection with
# perspective of satellite looking down at 50N, 100W.
# use low resolution coastlines.
map = Basemap(projection='ortho',lat_0=50,lon_0=-100,resolution='l')

# draw coastlines, country boundaries, fill continents.
map.drawcoastlines(linewidth=0.25)
map.drawcountries(linewidth=0.25)
map.fillcontinents(color='coral',lake_color='aqua')

# draw the edge of the map projection region (the projection limb)
map.drawmapboundary(fill_color='aqua')

# draw lat/lon grid lines every 30 degrees.
map.drawmeridians(np.arange(0,360,30))
map.drawparallels(np.arange(-90,90,30))

plt.title('contour lines over filled continent background')
plt.show()

# <headingcell level=1>

# Mercator

# <codecell>

# http://matplotlib.org/basemap/users/merc.html

from mpl_toolkits.basemap import Basemap
import numpy as np
import matplotlib.pyplot as plt
# llcrnrlat,llcrnrlon,urcrnrlat,urcrnrlon
# are the lat/lon values of the lower left and upper right corners
# of the map.
# lat_ts is the latitude of true scale.
# resolution = 'c' means use crude resolution coastlines.
m = Basemap(projection='merc',llcrnrlat=-80,urcrnrlat=80,\
            llcrnrlon=-180,urcrnrlon=180,lat_ts=20,resolution='c')
m.drawcoastlines()
m.fillcontinents(color='coral',lake_color='aqua')

# draw parallels and meridians.
m.drawparallels(np.arange(-90.,91.,30.))
m.drawmeridians(np.arange(-180.,181.,60.))
m.drawmapboundary(fill_color='aqua')
plt.title("Mercator Projection")
plt.show()

# <headingcell level=1>

# Lambert Azimuthal Equal Area Projection

# <codecell>

# http://matplotlib.org/basemap/users/laea.html

from mpl_toolkits.basemap import Basemap
import numpy as np
import matplotlib.pyplot as plt
# setup lambert azimuthal equal area basemap.
# lat_ts is latitude of true scale.
# lon_0,lat_0 is central point.
m = Basemap(width=12000000,height=8000000,
            resolution='l',projection='laea',\
            lat_ts=50,lat_0=50,lon_0=-107.)
m.drawcoastlines()
m.fillcontinents(color='coral',lake_color='aqua')
# draw parallels and meridians.
m.drawparallels(np.arange(-80.,81.,20.))
m.drawmeridians(np.arange(-180.,181.,20.))
m.drawmapboundary(fill_color='aqua')
# draw tissot's indicatrix to show distortion.
ax = plt.gca()
for y in np.linspace(m.ymax/20,19*m.ymax/20,9):
    for x in np.linspace(m.xmax/20,19*m.xmax/20,12):
        lon, lat = m(x,y,inverse=True)
        poly = m.tissot(lon,lat,1.5,100,\
                        facecolor='green',zorder=10,alpha=0.5)
plt.title("Lambert Azimuthal Equal Area Projection")
plt.show()

# <headingcell level=2>

# Lambert Conformal Projection (LCC)

# <codecell>

# http://matplotlib.org/basemap/users/lcc.html

from mpl_toolkits.basemap import Basemap
import numpy as np
import matplotlib.pyplot as plt
# setup lambert conformal basemap.
# lat_1 is first standard parallel.
# lat_2 is second standard parallel (defaults to lat_1).
# lon_0,lat_0 is central point.
# rsphere=(6378137.00,6356752.3142) specifies WGS4 ellipsoid
# area_thresh=1000 means don't plot coastline features less
# than 1000 km^2 in area.
m = Basemap(width=12000000,height=9000000,
            rsphere=(6378137.00,6356752.3142),\
            resolution='l',area_thresh=1000.,projection='lcc',\
            lat_1=45.,lat_2=55,lat_0=50,lon_0=-107.)
m.drawcoastlines()
m.fillcontinents(color='coral',lake_color='aqua')
# draw parallels and meridians.
m.drawparallels(np.arange(-80.,81.,20.))
m.drawmeridians(np.arange(-180.,181.,20.))
m.drawmapboundary(fill_color='aqua')
# draw tissot's indicatrix to show distortion.
ax = plt.gca()
for y in np.linspace(m.ymax/20,19*m.ymax/20,9):
    for x in np.linspace(m.xmax/20,19*m.xmax/20,12):
        lon, lat = m(x,y,inverse=True)
        poly = m.tissot(lon,lat,1.5,100,\
                        facecolor='green',zorder=10,alpha=0.5)
plt.title("Lambert Conformal Projection")
plt.show()

# <headingcell level=2>

# Equal area world map?

# <markdowncell>

# http://en.wikipedia.org/wiki/Cylindrical_equal-area_projection

# <markdowncell>

# http://matplotlib.org/basemap/users/mapsetup.html
# 
# > When a Basemap class instance is created, the desired map projection must be specified, along with information about the portion of the earth’s surface that the map projection will describe. There are two basic ways of doing this. One is to provide the latitude and longitude values of each of the four corners of the rectangular map projection region. The other is to provide the lat/lon value of the center of the map projection region along with the width and height of the region in map projection coordinates.

# <markdowncell>

# Note:  if I make width or height too big, I get complaints....but still not getting the whole 
# 
# https://www.google.com/search?q=circumference+earth
# 
# > 24,901 miles (40,075 km)

# <codecell>

from mpl_toolkits.basemap import Basemap
import numpy as np
import matplotlib.pyplot as plt
# setup lambert azimuthal equal area basemap.
# lat_ts is latitude of true scale.
# lon_0,lat_0 is central point.
m = Basemap(width=16200000,height=19500000,
            resolution='l',projection='laea',\
            lat_ts=0, lat_0=0,lon_0=0.)
m.drawcoastlines()
m.fillcontinents(color='coral',lake_color='aqua')
# draw parallels and meridians.
m.drawparallels(np.arange(-80.,81.,20.))
m.drawmeridians(np.arange(-180.,181.,20.))
m.drawmapboundary(fill_color='aqua')
# draw tissot's indicatrix to show distortion.
ax = plt.gca()
for y in np.linspace(m.ymax/20,19*m.ymax/20,9):
    for x in np.linspace(m.xmax/20,19*m.xmax/20,12):
        lon, lat = m(x,y,inverse=True)
        poly = m.tissot(lon,lat,1.5,100,\
                        facecolor='green',zorder=10,alpha=0.5)
plt.title("Lambert Azimuthal Equal Area Projection")
plt.show()

# <codecell>

# http://matplotlib.org/basemap/users/geography.html

from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
# setup Lambert Conformal basemap.
m = Basemap(width=12000000,height=9000000,projection='lcc',
            resolution='c',lat_1=45.,lat_2=55,lat_0=50,lon_0=-107.)
# draw coastlines.
m.drawcoastlines()
# draw a boundary around the map, fill the background.
# this background will end up being the ocean color, since
# the continents will be drawn on top.
m.drawmapboundary(fill_color='aqua')
# fill continents, set lake color same as ocean color.
m.fillcontinents(color='coral',lake_color='aqua')
plt.show()

# <codecell>

from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
# setup Lambert Conformal basemap.
# set resolution=None to skip processing of boundary datasets.
m = Basemap(width=12000000,height=9000000,projection='lcc',
            resolution=None,lat_1=45.,lat_2=55,lat_0=50,lon_0=-107.)
# draw a land-sea mask for a map background.
# lakes=True means plot inland lakes with ocean color.

try:
    m.drawlsmask(land_color='coral',ocean_color='aqua',lakes=True)
    plt.show()
except Exception, e:
    print e

# <codecell>

# for some reason -- this doesn't work for me
# bluemarble doesn't look right

from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
# setup Lambert Conformal basemap.
# set resolution=None to skip processing of boundary datasets.
#m = Basemap(width=12000000,height=9000000,projection='lcc',
#            resolution=None,lat_1=45.,lat_2=55.,lat_0=45.,lon_0=-107.)

m = Basemap(width=12000000,height=9000000,projection='lcc',
            resolution='c',lat_1=45.,lat_2=55,lat_0=50,lon_0=-107.)

m.bluemarble()
plt.show()

# <codecell>

# for some reason -- this doesn't work for me
# shadedrelief doesn't look right


from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
# setup Lambert Conformal basemap.
# set resolution=None to skip processing of boundary datasets.
#m = Basemap(width=12000000,height=9000000,projection='lcc',
#            resolution=None,lat_1=45.,lat_2=55,lat_0=50,lon_0=-107.)

m = Basemap(width=12000000,height=9000000,
            rsphere=(6378137.00,6356752.3142),\
            resolution='l',area_thresh=1000.,projection='lcc',\
            lat_1=45.,lat_2=55,lat_0=50,lon_0=-107.)

try:
    m.shadedrelief()
    plt.show()
except Exception as e:
    print e

# <codecell>

# for some reason -- this doesn't work for me
# etopo doesn't look right


from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
# setup Lambert Conformal basemap.
# set resolution=None to skip processing of boundary datasets.
m = Basemap(width=12000000,height=9000000,projection='lcc',
            resolution=None,lat_1=45.,lat_2=55,lat_0=50,lon_0=-107.)
m.etopo()
plt.show()

# <codecell>

# http://matplotlib.org/basemap/users/mapcoords.html

from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import numpy as np

# setup Lambert Conformal basemap.
m = Basemap(width=12000000,height=9000000,projection='lcc',
            resolution='c',lat_1=45.,lat_2=55,lat_0=50,lon_0=-107.)

# draw a boundary around the map, fill the background.
# this background will end up being the ocean color, since
# the continents will be drawn on top.
m.drawmapboundary(fill_color='aqua')
# fill continents, set lake color same as ocean color.
m.fillcontinents(color='coral',lake_color='aqua')

# draw state boundaries too
# http://matplotlib.org/basemap/api/basemap_api.html#mpl_toolkits.basemap.Basemap.drawstates
m.drawstates(linewidth=0.1)


# draw parallels and meridians.
# label parallels on right and top
# meridians on bottom and left
parallels = np.arange(0.,81,10.)
# labels = [left,right,top,bottom]
m.drawparallels(parallels,labels=[False,True,True,False])
meridians = np.arange(10.,351.,20.)
m.drawmeridians(meridians,labels=[True,False,False,True])


# plot blue dot on Boulder, colorado and label it as such.
lon, lat = -104.237, 40.125 # Location of Boulder
# convert to map projection coords.
# Note that lon,lat can be scalars, lists or numpy arrays.
xpt,ypt = m(lon,lat)
# convert back to lat/lon
lonpt, latpt = m(xpt,ypt,inverse=True)
m.plot(xpt,ypt,'bo')  # plot a blue dot there
# put some text next to the dot, offset a little bit
# (the offset is in map projection coordinates)
plt.text(xpt+100000,ypt+100000,'Boulder (%5.1fW,%3.1fN)' % (lonpt,latpt))
plt.show()

# <codecell>

# https://github.com/matplotlib/basemap/blob/master/examples/fillstates.py



import zipfile
import os


from __future__ import print_function
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap as Basemap
from matplotlib.colors import rgb2hex
from matplotlib.patches import Polygon

shp_info_path = os.path.join(os.pardir, "data/census/st99_d00")

# Lambert Conformal map of lower 48 states.
m = Basemap(llcrnrlon=-119,llcrnrlat=22,urcrnrlon=-64,urcrnrlat=49,
            projection='lcc',lat_1=33,lat_2=45,lon_0=-95)
# draw state boundaries.
# data from U.S Census Bureau
# http://www.census.gov/geo/www/cob/st2000.html


shp_info = m.readshapefile(shp_info_path,'states',drawbounds=True)
# population density by state from
# http://en.wikipedia.org/wiki/List_of_U.S._states_by_population_density
popdensity = {
'New Jersey':  438.00,
'Rhode Island':   387.35,
'Massachusetts':   312.68,
'Connecticut':	  271.40,
'Maryland':   209.23,
'New York':    155.18,
'Delaware':    154.87,
'Florida':     114.43,
'Ohio':	 107.05,
'Pennsylvania':	 105.80,
'Illinois':    86.27,
'California':  83.85,
'Hawaii':  72.83,
'Virginia':    69.03,
'Michigan':    67.55,
'Indiana':    65.46,
'North Carolina':  63.80,
'Georgia':     54.59,
'Tennessee':   53.29,
'New Hampshire':   53.20,
'South Carolina':  51.45,
'Louisiana':   39.61,
'Kentucky':   39.28,
'Wisconsin':  38.13,
'Washington':  34.20,
'Alabama':     33.84,
'Missouri':    31.36,
'Texas':   30.75,
'West Virginia':   29.00,
'Vermont':     25.41,
'Minnesota':  23.86,
'Mississippi':	 23.42,
'Iowa':	 20.22,
'Arkansas':    19.82,
'Oklahoma':    19.40,
'Arizona':     17.43,
'Colorado':    16.01,
'Maine':  15.95,
'Oregon':  13.76,
'Kansas':  12.69,
'Utah':	 10.50,
'Nebraska':    8.60,
'Nevada':  7.03,
'Idaho':   6.04,
'New Mexico':  5.79,
'South Dakota':	 3.84,
'North Dakota':	 3.59,
'Montana':     2.39,
'Wyoming':      1.96,
'Alaska':     0.42}
print(shp_info)
# choose a color for each state based on population density.
colors={}
statenames=[]
cmap = plt.cm.hot # use 'hot' colormap
vmin = 0; vmax = 450 # set range.
print(m.states_info[0].keys())
for shapedict in m.states_info:
    statename = shapedict['NAME']
    # skip DC and Puerto Rico.
    if statename not in ['District of Columbia','Puerto Rico']:
        pop = popdensity[statename]
        # calling colormap with value between 0 and 1 returns
        # rgba value.  Invert color range (hot colors are high
        # population), take sqrt root to spread out colors more.
        colors[statename] = cmap(1.-np.sqrt((pop-vmin)/(vmax-vmin)))[:3]
    statenames.append(statename)
# cycle through state names, color each one.
ax = plt.gca() # get current axes instance
for nshape,seg in enumerate(m.states):
    # skip DC and Puerto Rico.
    if statenames[nshape] not in ['District of Columbia','Puerto Rico']:
        color = rgb2hex(colors[statenames[nshape]]) 
        poly = Polygon(seg,facecolor=color,edgecolor=color)
        ax.add_patch(poly)
# draw meridians and parallels.
m.drawparallels(np.arange(25,65,20),labels=[1,0,0,0])
m.drawmeridians(np.arange(-120,-40,20),labels=[0,0,0,1])
plt.title('Filling State Polygons by Population Density')
plt.show()

# <headingcell level=1>

# Haiti

# <markdowncell>

# http://my.safaribooksonline.com/book/programming/python/9781449323592/8dot-plotting-and-visualization/id2805177

# <codecell>

import os

HAITI_PATH = os.path.join(os.pardir, "pydata-book", "ch08", "Haiti.csv")

assert os.path.exists(HAITI_PATH)

# <codecell>

import os
import pandas as pd
from pandas import DataFrame, Series

data = pd.read_csv(HAITI_PATH)

# <codecell>

data[['INCIDENT DATE', 'LATITUDE', 'LONGITUDE']][:10]

# <codecell>

data['CATEGORY'][:6]

# <codecell>

data.describe()

# <codecell>

data = data[(data.LATITUDE > 18) & (data.LATITUDE < 20) &
            (data.LONGITUDE > -75) & (data.LONGITUDE < -70)
            & data.CATEGORY.notnull()]

# <codecell>

def to_cat_list(catstr):
    stripped = (x.strip() for x in catstr.split(','))
    return [x for x in stripped if x]

def get_all_categories(cat_series):
    cat_sets = (set(to_cat_list(x)) for x in cat_series)
    return sorted(set.union(*cat_sets))

def get_english(cat):
	code, names = cat.split('.')
	if '|' in names:
		names = names.split(' | ')[1]
	return code, names.strip()

# <codecell>

get_english('2. Urgences logistiques | Vital Lines')

# <codecell>

all_cats = get_all_categories(data.CATEGORY)

english_mapping = dict(get_english(x) for x in all_cats)

# <codecell>

def get_code(seq):
    return [x.split('.')[0] for x in seq if x]

all_codes = get_code(all_cats)
code_index = pd.Index(np.unique(all_codes))
dummy_frame = DataFrame(np.zeros((len(data), len(code_index))),
                        index=data.index, columns=code_index)

# <codecell>

dummy_frame.ix[:, :6]

# <codecell>

for row, cat in zip(data.index, data.CATEGORY):
    codes = get_code(to_cat_list(cat))
    dummy_frame.ix[row, codes] = 1

data = data.join(dummy_frame.add_prefix('category_'))

# <codecell>

data.CATEGORY.isnull().value_counts()

# <codecell>

from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt

def basic_haiti_map(ax=None, lllat=17.25, urlat=20.25,
                    lllon=-75, urlon=-71):
    # create polar stereographic Basemap instance.
    m = Basemap(ax=ax, projection='stere',
                lon_0=(urlon + lllon) / 2,
                lat_0=(urlat + lllat) / 2,
                llcrnrlat=lllat, urcrnrlat=urlat,
                llcrnrlon=lllon, urcrnrlon=urlon,
                resolution='f')
    # draw coastlines, state and country boundaries, edge of map.
    m.drawcoastlines()
    m.drawstates()
    m.drawcountries()
    return m

# <codecell>

fig, axes = plt.subplots(nrows=2, ncols=2, figsize=(12, 10))
fig.subplots_adjust(hspace=0.05, wspace=0.05)

to_plot = ['2a', '1', '3c', '7a']

lllat=17.25; urlat=20.25; lllon=-75; urlon=-71

for code, ax in zip(to_plot, axes.flat):
	m = basic_haiti_map(ax, lllat=lllat, urlat=urlat,
						lllon=lllon, urlon=urlon)

	cat_data = data[data['category_%s' % code] == 1]

    # compute map proj coordinates.
	x, y = m(cat_data.LONGITUDE, cat_data.LATITUDE)

	m.plot(x, y, 'k.', alpha=0.5)
	ax.set_title('%s: %s' % (code, english_mapping[code]))
    
plt.show()

# <codecell>

# high res data
# http://magician.ucsd.edu/Software/PmagPy/hires.html
from mpl_toolkits.basemap import basemap_datadir; print basemap_datadir

# <codecell>


