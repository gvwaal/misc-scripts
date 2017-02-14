# misc-scripts
Contains various scripts I've created for various purposes.

WatershedSummarizer.py: Created for a client who was working with a set of fluxes stored in netCDF files in ArcMap. Given a set of netCDF files in a directory, the script converts the netCDF files to rasters and uses the Zonal Statistics with a supplied zone layer. The created tables are then merged together into a single dBASE table, then converted to an .xls spreadsheet in the chosen output directory.
