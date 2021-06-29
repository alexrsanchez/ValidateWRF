# ValidateWRF
Repository dedicated to WRF model runs validation purposes

# Usage
An important part of making a meteorological prediction is to validate your model so it is able to predict as best as possible the target phenomenon or phenomena. In this sense ERA5 reanalysis database, developed by ECMWF, is such a great product for spatial validation. But other choices are available, such as NCEP reanalysis.

To download ERA5 data, you can use the ERA5_download.py script in which you can select the dates, pressure levels and variables to extract from the ERA5 database in a single file. You can also change the format of the file (netCDF is default) and the area (as an array with the limit points [N,W,S,E]) covered by the extraction.

Having two datasets -one of your simulation and one reanalysis- it's easy to analise the spatial behaviour of your simulation using the _xarray_ python package. The only issue is to match the spatial resolutions of the WRF simulation file and the ERA5 file. The ERA5 database has an horizontal resolution of 31km, while WRF model is usually run at higher resolutions of about 1-10 km. As a first approximation, the main script **evaluate_WRF.py** uses _xshape_ to interpolate the coarser resolution data to match the higher resolution data file. Careful must be taken though, because in some cases interpolation may not reflect the reality.
Once having data at the same resolution, the script provides some useful statistics to analise the spatial behaviour of the WRF simulation.

# Python environment

To launch the Python script, I recommend you to create a conda environment for exclusive use of this script in where you will install just the necessary python libraries needed by the **evaluate_WRF.py** script. This can be done as follows:
```
conda env create -f WRFvalidation_env.yml
```

The *WRFvalidation_env.yml* file will install all the packages needed for running the scripts in this project.


Then activate the environment by typing ``` conda activate WRFvalidation_env``` in the commands line. 

Now you can launch the script and analise your WRF model simulations!

# License

The project is licensed under the MIT license.
