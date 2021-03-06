# misc-scripts
Contains scripts I've created for various purposes. All are licensed under the MIT License unless otherwise noted.

## dem_fetch.py
Created to download DEMs from URLs stored in a text file.

**todo:** Mosaic unzipped files together with arcpy?

## FireStation.py
Initially created to expidite the process of determining response times from fire departments. A geodatabase with multiple sets of points is provided by the user and the script loops through it, using Network Analyst to determine response times with 5, 10, and 15 minute breaks.

**todo:** Fix the last bug. File name generation isn't working right and the final layer gets overwritten instead of making a new one.

## gcs2pcs.py
I created this to convert a bunch of feature classes stored in a geodatabase from a geographic coordinate system to a projected coordinate system. The script loops through a given geodatabase, converts the feature classes, and saves them to the desired output location.

**todo:** Nothing, though I may add features in the future if need arises.

## mosaic.py
Quick-and-dirty script to mosaic together a bunch of DEMs in an odd directory configuration. Manually running the tool would have involved too much clicking.

**todo:** Could make things a little nicer looking, such as replacing gdb_list with a long string on line 18.

## WatershedSummarizer.py
Created for a client who was working with a set of fluxes stored in netCDF files. Given a set of netCDF files in a directory, the script converts the netCDF files to rasters and uses the Zonal Statistics tool with a supplied zone layer. The created dBASE tables are then merged together into a single dBASE table, then converted to an .xls spreadsheet in the chosen output directory.

**todo:** Clean up the code, it's a bit hard to read at the moment.
