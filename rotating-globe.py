import datetime,matplotlib,time
from mpl_toolkits.basemap import Basemap,shiftgrid
import matplotlib.pyplot as plt
import numpy as np
from gifly import gif_maker

def plot_topo(map,cmap=plt.cm.jet):
    #20 minute bathymetry/topography data
    etopo = np.loadtxt('topo/etopo20data.gz')
    lons  = np.loadtxt('topo/etopo20lons.gz')
    lats  = np.loadtxt('topo/etopo20lats.gz')
    # shift data so lons go from -180 to 180 instead of 20 to 380.
    etopo,lons = shiftgrid(180.,etopo,lons,start=False)
    lons, lats = np.meshgrid(lons, lats)
    cs = map.pcolormesh(lons,lats,etopo,cmap=cmap,latlon=True,shading='gouraud')


## Codes from https://makersportal.com/blog/2018/8/16/rotating-globe-in-python-using-basemap-toolkit
# plt.ion() allows python to update its figures in real-time
plt.ion()
fig = plt.figure(figsize=(9,6))

# set the latitude angle steady, and vary the longitude. You can also reverse this to
# create a rotating globe latitudinally as well
lat_viewing_angle = [20.0,20.0]
lon_viewing_angle = [-180,180]
rotation_steps = 100
lat_vec = np.linspace(lat_viewing_angle[0],lat_viewing_angle[0],rotation_steps)
lon_vec = np.linspace(lon_viewing_angle[0],lon_viewing_angle[1],rotation_steps)

# for making the gif animation
gif_indx = 0

# loop through the longitude vector above
for pp in range(0,len(lat_vec)):    
    print("{}/{}".format(pp,len(lat_vec)))
    plt.cla()
    m = Basemap(projection='ortho', 
              lat_0=lat_vec[pp], lon_0=lon_vec[pp])
    m.drawcoastlines(linewidth=0.5)
    # m.drawcountries()
    plot_topo(m)
    #show the plot, introduce a small delay to allow matplotlib to catch up
    plt.show()
    plt.pause(0.01)
    # iterate to create the GIF animation
    gif_maker('basemap_rotating_globe.gif','./png_dir/',gif_indx,len(lat_vec)-1,dpi=90)
    gif_indx+=1