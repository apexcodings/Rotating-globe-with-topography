import datetime,matplotlib,time
from mpl_toolkits.basemap import Basemap,shiftgrid
import matplotlib.pyplot as plt
import numpy as np
from gifly import gif_maker
import os, glob

def plot_topo(map,cmap=plt.cm.jet):
    #20 minute bathymetry/topography data
    etopo = np.loadtxt('topo/etopo20data.gz')
    lons  = np.loadtxt('topo/etopo20lons.gz')
    lats  = np.loadtxt('topo/etopo20lats.gz')
    # shift data so lons go from -180 to 180 instead of 20 to 380.
    etopo,lons = shiftgrid(180.,etopo,lons,start=False)
    lons, lats = np.meshgrid(lons, lats)
    cs = map.pcolormesh(lons,lats,etopo,cmap=cmap,latlon=True,shading='gouraud')

files = glob.glob('png_dir/*.png')
for f in files:
    os.remove(f)

# plt.ion() allows python to update its figures in real-time
plt.ion()
dpi=80
fig = plt.figure(dpi=dpi)

# set the latitude angle steady, and vary the longitude. You can also reverse this to
# create a rotating globe latitudinally as well
lat_viewing_angle = [20.0,20.0]
lon_viewing_angle = [-180,180]
rotation_steps = 360
lat_vec = np.linspace(lat_viewing_angle[0],lat_viewing_angle[0],rotation_steps)
lon_vec = np.linspace(lon_viewing_angle[0],lon_viewing_angle[1],rotation_steps)

# for making the gif animation
gif_indx = 0

# loop through the longitude vector above
for pp in range(0,len(lat_vec)):    
    plt.cla()
    m = Basemap(projection='ortho', lat_0=lat_vec[pp], lon_0=lon_vec[pp])
    m.drawcoastlines(linewidth=0.5)
    # m.drawcountries()
    plot_topo(m)
    
    # iterate to create the GIF animation
    gif_maker('basemap_rotating_globe.gif','./png_dir/',gif_indx,len(lat_vec)-1,dpi=dpi)
    gif_indx+=1
    print("{}/{}".format(pp,len(lat_vec)))