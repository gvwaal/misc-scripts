# misc-scripts
Contains various scripts I've created for various purposes. All are licensed under the MIT License unless otherwise noted.

## WatershedSummarizer.py
Created for a client who was working with a set of fluxes stored in netCDF files. Given a set of netCDF files in a directory, the script converts the netCDF files to rasters and uses the Zonal Statistics tool with a supplied zone layer. The created dBASE tables are then merged together into a single dBASE table, then converted to an .xls spreadsheet in the chosen output directory.

**todo:** clean up the code, it's a bit hard to read at the moment.

## gcs2pcs.py
I created this to convert a bunch of feature classes stored in a geodatabase from a geographic coordinate system to a projected coordinate system. The script loops through a given geodatabase, converts the feature classes, and saves them to the desired output location.

**todo:** nothing, though I may add features in the future if need arises.
