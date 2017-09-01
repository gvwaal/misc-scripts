# misc-scripts
Contains scripts I've created for various purposes. All are licensed under the MIT License unless otherwise noted.

## dem_fetch.py
Created to grab a bunch of DEMs from a FTP server.

**todo:** Ensure the script saves the zipped geodatabases correctly. Add unzipping functionality?

## FireStation.py
Initially created to expidite the process of determining response times from fire departments. A geodatabase with multiple sets of points is provided by the user and the script loops through it, using Network Analyst to determine response times with 5, 10, and 15 minute breaks.

**todo:** Fix the last bug. File name generation isn't working right and the final layer gets overwritten instead of making a new one.

## gcs2pcs.py
I created this to convert a bunch of feature classes stored in a geodatabase from a geographic coordinate system to a projected coordinate system. The script loops through a given geodatabase, converts the feature classes, and saves them to the desired output location.

**todo:** Nothing, though I may add features in the future if need arises.

## WatershedSummarizer.py
Created for a client who was working with a set of fluxes stored in netCDF files. Given a set of netCDF files in a directory, the script converts the netCDF files to rasters and uses the Zonal Statistics tool with a supplied zone layer. The created dBASE tables are then merged together into a single dBASE table, then converted to an .xls spreadsheet in the chosen output directory.

**todo:** Clean up the code, it's a bit hard to read at the moment.
