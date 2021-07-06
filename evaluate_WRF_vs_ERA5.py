# -*- coding: utf-8 -*-

###################################################
##### Script by: Alejandro Rodríguez Sánchez ######
##### 					     ######
##### Contact: alejandro.rodriguez@ciemat.es ######
###################################################

import xesmf as xe
import xarray as xr
import numpy as np
import matplotlib
#matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from datetime import datetime , timedelta 
import cartopy.crs as ccrs
import xshape
from calculate_spatial_statistics import calculate_statistics

domain = 'ESP09'
plotdir='/auto_nfs/calaire9/PRECOZ/evaluate_WRF/'+domain+'/'


ERA5data = xr.open_dataset('/auto_nfs/calaire9/PRECOZ/ERA5/ERA5_ESP09_20190226_20190228.nc')
ERA5variables = ERA5data.variables
print(ERA5variables)
print(ERA5data)

WRFdata = xr.open_dataset('/auto_nfs/calaire9/PRECOZ/WRF_desarrollo_out/WRFOUT_'+domain+'_20190226_20190228_2021-07-02_09-26.nc')
WRFvariables = WRFdata.variables

#elif domain=="ESP09":
#    ERA5data = xr.open_dataset('/auto_nfs/calaire9/PRECOZ/ERA5/ERA5_ESP09_20190226_20190228.nc')
#    ERA5variables = ERA5data.variables
#    print(ERA5variables)
#    print(ERA5data)
#
#    WRFdata = xr.open_dataset('/auto_nfs/calaire9/PRECOZ/WRF_desarrollo_out/WRFOUT_ZAR003_20190226_20190228_2021-06-23_12-23.nc')
#    WRFvariables = WRFdata.variables

# Rename ERA5data variables to match with WRF names and perform arithmetics between two xarray-datasets
ERA5data = ERA5data.rename({'t2m': 'T2', 'tcc': 'CFRACT', 'u10': 'U10', 'v10': 'V10'})

# Set lat and lon coordinates to WRF instead of south_north and west_east
minWRFlat = WRFdata.XLAT.min().values
maxWRFlat = WRFdata.XLAT.max().values
minWRFlon = WRFdata.XLONG.min().values
maxWRFlon = WRFdata.XLONG.max().values

lat_WRF = np.linspace(minWRFlat,maxWRFlat,WRFdata.south_north.max().values+1)
long_WRF = np.linspace(minWRFlon,maxWRFlon,WRFdata.west_east.max().values+1)

# Rename coordinates names to match the ERA5 coordinates names
WRFdata = WRFdata.swap_dims({'Time': 'XTIME'})
WRFdata['west_east'] = long_WRF
WRFdata['south_north'] = lat_WRF
WRFdata = WRFdata.rename({'XTIME': 'time', 'south_north': 'latitude', 'west_east': 'longitude'}).set_coords(['longitude', 'latitude','time'])

print(WRFdata.T2)

# Interpolate ERA5 data to match WRF data extension
ERA5data_highres = ERA5data.interp(latitude=WRFdata["latitude"], longitude=WRFdata["longitude"])

print(len(WRFdata.time))
print(len(ERA5data_highres.time))

if len(ERA5data_highres.time)>len(WRFdata.time):
    ERA5data_highres = ERA5data_highres.isel(time=slice(0, len(WRFdata.time)))
elif len(ERA5data_highres.time)<len(WRFdata.time):
    WRFdata = WRFdata.isel(time=slice(0, len(ERA5data_highres.time)))

print(ERA5data_highres)

#import xshape


# Compute maps of statistics between WRF and ERA5
########
## T2 ##
########

from cartopy.io.shapereader import Reader
from cartopy.feature import ShapelyFeature

print(WRFdata.T2)
print(ERA5data_highres.T2)

variables = ['CFRACT','T2']#,'U10','V10']
tiempos = np.arange(36,41,1)
for j in range(len(tiempos)):
    for i in range(len(variables)):
        WRF_minus_ERA5 = WRFdata[variables[i]] - ERA5data_highres[variables[i]]
        print(WRF_minus_ERA5)
    


        RMSE_WRF, bias_WRF, MAE_WRF = calculate_statistics(WRFdata[variables[i]],ERA5data_highres[variables[i]])


        # Plot maps
        map_proj = ccrs.LambertConformal(central_longitude=-1, central_latitude=41.5)
        map_proj = ccrs.UTM(zone=30)
        #p = ERA5data[variables[i]].isel(time=tiempos[j]).plot(transform=ccrs.PlateCarree(),  # the data's projection
        #        subplot_kws={'projection': map_proj})
#        p=ERA5data[variables[i]].isel(time=tiempos[j]).xshape.overlay('/home/alejandro/Documentos/Doctorado/SHP_ETRS89/ll_provinciales_inspire_peninbal_etrs89/ll_provinciales_inspire_peninbal_etrs89.shp')#, subplot_kws={'projection': map_proj})
        p = ERA5data[variables[i]].isel(time=tiempos[j]).xshape.overlay('/auto_nfs/calaire9/PRECOZ/evaluate_WRF/datos_geoespaciales/shapefiles/NUTS_RG_01M_2021_4326_LEVL_3.shp/NUTS_RG_01M_2021_4326_LEVL_3_lines.shp',  cbar_kwargs={
        "orientation": "vertical",
        "shrink": 0.85,
        "aspect": 31,
        #"label": "%s difference " %variables[i],
        },)
        p.axes.set_xlim(max(ERA5data.longitude.min().values,WRFdata.longitude.min().values), min(ERA5data.longitude.max().values,WRFdata.longitude.max().values))
        p.axes.set_ylim(max(ERA5data.latitude.min().values,WRFdata.latitude.min().values), min(ERA5data.latitude.max().values,WRFdata.latitude.max().values))
        p.axes.set_title('ERA5 %s. Time:%s' %(variables[i],ERA5data.T2.time[tiempos[j]].values.astype('datetime64[s]')))
        plt.tight_layout()
        plt.savefig(plotdir+'ERA5_%s_timestep_%s.png' %(variables[i],tiempos[j]),dpi=300)
        plt.show()
        

        map_proj = ccrs.LambertConformal(central_longitude=-1, central_latitude=41.5)
        map_proj = ccrs.UTM(zone=30)
        p = ERA5data_highres[variables[i]].isel(time=tiempos[j]).xshape.overlay('/auto_nfs/calaire9/PRECOZ/evaluate_WRF/datos_geoespaciales/shapefiles/NUTS_RG_01M_2021_4326_LEVL_3.shp/NUTS_RG_01M_2021_4326_LEVL_3_lines.shp',  cbar_kwargs={
        "orientation": "vertical",
        "shrink": 0.85,
        "aspect": 31,
        #"label": "%s difference " %variables[i],
        },)
        p.axes.set_xlim(max(ERA5data.longitude.min().values,WRFdata.longitude.min().values), min(ERA5data.longitude.max().values,WRFdata.longitude.max().values))
        p.axes.set_ylim(max(ERA5data.latitude.min().values,WRFdata.latitude.min().values), min(ERA5data.latitude.max().values,WRFdata.latitude.max().values))
        p.axes.set_title('ERA5 interpolated %s. Time:%s' %(variables[i],ERA5data.T2.time[tiempos[j]].values.astype('datetime64[s]')))
        plt.tight_layout()     
        plt.savefig(plotdir+'ERA5interpolated_%s_timestep_%s.png' %(variables[i],tiempos[j]),dpi=300)
        plt.show()


        map_proj = ccrs.LambertConformal(central_longitude=-1, central_latitude=41.5)
        map_proj = ccrs.UTM(zone=30)
        p = WRFdata[variables[i]].isel(time=tiempos[j]).xshape.overlay('/auto_nfs/calaire9/PRECOZ/evaluate_WRF/datos_geoespaciales/shapefiles/NUTS_RG_01M_2021_4326_LEVL_3.shp/NUTS_RG_01M_2021_4326_LEVL_3_lines.shp',  cbar_kwargs={
        "orientation": "vertical",
        "shrink": 0.85,
        "aspect": 31,
        #"label": "%s difference " %variables[i],
        },)
        p.axes.set_xlim(max(ERA5data.longitude.min().values,WRFdata.longitude.min().values), min(ERA5data.longitude.max().values,WRFdata.longitude.max().values))
        p.axes.set_ylim(max(ERA5data.latitude.min().values,WRFdata.latitude.min().values), min(ERA5data.latitude.max().values,WRFdata.latitude.max().values))
        p.axes.set_title('WRF %s. Time:%s' %(variables[i],ERA5data.T2.time[tiempos[j]].values.astype('datetime64[s]')))
        plt.tight_layout()     
        plt.savefig(plotdir+'WRF_%s_timestep_%s.png' %(variables[i],tiempos[j]),dpi=300)
        plt.show()
    

        map_proj = ccrs.LambertConformal(central_longitude=-1, central_latitude=41.5)
        map_proj = ccrs.UTM(zone=30)
        p = WRF_minus_ERA5.isel(time=tiempos[j]).xshape.overlay('/auto_nfs/calaire9/PRECOZ/evaluate_WRF/datos_geoespaciales/shapefiles/NUTS_RG_01M_2021_4326_LEVL_3.shp/NUTS_RG_01M_2021_4326_LEVL_3_lines.shp',  cbar_kwargs={
        "orientation": "vertical",
        "shrink": 0.85,
        "aspect": 31,
        "label": "%s difference " %variables[i],
        },)
        p.axes.set_xlim(max(ERA5data.longitude.min().values,WRFdata.longitude.min().values), min(ERA5data.longitude.max().values,WRFdata.longitude.max().values))
        p.axes.set_ylim(max(ERA5data.latitude.min().values,WRFdata.latitude.min().values), min(ERA5data.latitude.max().values,WRFdata.latitude.max().values))
        p.axes.set_title('WRF - ERA5 interpolated %s. Time:%s' %(variables[i],ERA5data.T2.time[tiempos[j]].values.astype('datetime64[s]')))
        plt.tight_layout()             
        plt.savefig(plotdir+'WRF_ERA5_%sdiff_timestep_%s.png' %(variables[i],tiempos[j]),dpi=300)
        plt.show()


        map_proj = ccrs.LambertConformal(central_longitude=-1, central_latitude=41.5)
        map_proj = ccrs.UTM(zone=30)
        p = RMSE_WRF.xshape.overlay('/auto_nfs/calaire9/PRECOZ/evaluate_WRF/datos_geoespaciales/shapefiles/NUTS_RG_01M_2021_4326_LEVL_3.shp/NUTS_RG_01M_2021_4326_LEVL_3_lines.shp',  cmap=matplotlib.cm.Reds , cbar_kwargs={
        "orientation": "vertical",
        "shrink": 0.85,
        "aspect": 31,
        "label": "%s RMSE " %variables[i],
        },)
        p.axes.set_xlim(max(ERA5data.longitude.min().values,WRFdata.longitude.min().values), min(ERA5data.longitude.max().values,WRFdata.longitude.max().values))
        p.axes.set_ylim(max(ERA5data.latitude.min().values,WRFdata.latitude.min().values), min(ERA5data.latitude.max().values,WRFdata.latitude.max().values))
        p.axes.set_title('WRF RMSE %s. Time: All simulation' %(variables[i]))
        plt.tight_layout()     
        plt.savefig(plotdir+'WRF_%sRMSE.png' %(variables[i]),dpi=300)
        plt.show()
    
        map_proj = ccrs.LambertConformal(central_longitude=-1, central_latitude=41.5)
        map_proj = ccrs.UTM(zone=30)
        p = bias_WRF.xshape.overlay('/auto_nfs/calaire9/PRECOZ/evaluate_WRF/datos_geoespaciales/shapefiles/NUTS_RG_01M_2021_4326_LEVL_3.shp/NUTS_RG_01M_2021_4326_LEVL_3_lines.shp',  cmap=matplotlib.cm.seismic , cbar_kwargs={
        "orientation": "vertical",
        "shrink": 0.85,
        "aspect": 31,
        "label": "%s bias " %variables[i],
        },)
        p.axes.set_xlim(max(ERA5data.longitude.min().values,WRFdata.longitude.min().values), min(ERA5data.longitude.max().values,WRFdata.longitude.max().values))
        p.axes.set_ylim(max(ERA5data.latitude.min().values,WRFdata.latitude.min().values), min(ERA5data.latitude.max().values,WRFdata.latitude.max().values))
        p.axes.set_title('WRF bias %s. Time: All simulation' %(variables[i]))
        plt.tight_layout()     
        plt.savefig(plotdir+'WRF_%sbias.png' %(variables[i]),dpi=300)
        plt.show()


    # Plotting several timesteps in one plot
        g_simple = WRFdata[variables[i]].plot(x="longitude", y="latitude", col="time", col_wrap=4)
        plt.tight_layout()
        plt.show()
