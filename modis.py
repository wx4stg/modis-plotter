#!/usr/bin/env python3
# Plotting MODIS csv files
# Created 26 May 2022 by Sam Gardner <stgardner4@tamu.edu>

import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from cartopy import crs as ccrs
from cartopy import feature as cfeat

def plotSatellite(name):
    data = pd.read_csv(name+".csv", header=None)
    lats = data[0].to_numpy()[1:].astype(float)
    lons = data.iloc[[0]].to_numpy()[0][1:].astype(float)
    data = data.iloc[1:, 1:].to_numpy()
    data = np.ma.masked_array(data, mask=np.where(data==99999, 1, 0))
    fig = plt.figure()
    px = 1/plt.rcParams["figure.dpi"]
    fig.set_size_inches(1280*px, 720*px)
    ax = plt.axes(projection=ccrs.PlateCarree(3857))
    pcm = ax.pcolormesh(lons, lats, data, cmap="plasma", transform=ccrs.PlateCarree())
    ax.add_feature(cfeat.COASTLINE.with_scale("50m"), linewidth=0.5)
    ax.set_extent([-64.543198, -54.543198, 10.193887, 16.193887])
    ax.set_position([0.05, 0.11, .9, .85])
    cbax = fig.add_axes([(ax.get_position().width/2)-(ax.get_position().width/6),0.075,(ax.get_position().width/3),.02])
    fig.colorbar(pcm, cax=cbax, orientation="horizontal", label="AOT", extend="neither")
    cbax.set_position([(ax.get_position().width/2)+ax.get_position().x0-(cbax.get_position().width/2), cbax.get_position(). y0,cbax.get_position().width, cbax.get_position().height])
    ax.set_title("Aerosol Optical Thickness (1 DAY - "+name.upper()+"/MODIS)")
    fig.savefig(name+".png")

if __name__ == "__main__":
    plotSatellite("aqua")
    plotSatellite("terra")
