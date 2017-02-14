# Purpose: Given a set of netCDF files in a directory, converts the netCDF files to rasters and
# uses the Zonal Statistics with a supplied zone layer. The created tables are then merged together
# into a single dBASE table, then converted to an .xls spreadsheet in the chose output directory.
#
# Version: 1.0
#
# Requires: Spatial Analyst extension for ArcMap, pre-created input and output directories, and
# a supplied zone layer.
#
# Author: Gerrit VanderWaal

# Imports os module.
print "Importing os module..."
import os

# Imports arcpy module (akin to libraries for C or C++).
print "Importing arcpy module...\n"
import arcpy

# Creates custom exception error to be used in case the Spatial Analyst license is unavailable. This section does nothing but is called later.
# in the script if needed. See https://docs.python.org/2.7/tutorial/errors.html for more info.
class LicenseError(Exception):
    pass

# Checks that the Spatial Analyst extension is installed, calls the LicenseError exception if it is not.
print "Checking Spatial Analyst license..."
if arcpy.CheckExtension("Spatial") == "Available":
    arcpy.CheckOutExtension("Spatial")
    print "License retrieved.\n"
else:
    raise LicenseError

# Main program component.
try:

    # Enables data overwriting.
    print "Overwriting of data enabled.\n"
    arcpy.env.overwriteOutput = True
    
    # Sets the workspace that the script will take in files from.
    inputSpace = raw_input("Enter directory containing netCDF files as a complete filepath: ")
    arcpy.env.workspace = inputSpace

    # Sets default output directory that files will be deposited in.
    outputSpace = raw_input("Enter directory where resulting data will be stored (complete filepath): ")
    
    # Sets zone locations for use in Zonal Statistics tool.
    zones = raw_input("Enter layer to be used as zones in Zonal Statistics (complete filepath): ")
    
    # Stores netCDF files in variable fileList
    fileList = os.listdir(inputSpace)
    
    # Creates new table that rest of tables will be appended to, with the year as the title
    print "\nCreating summary table...\n"
    period = fileList[0].find(".")
    summaryFile = "Summary_" + fileList[0][period+1:period+5]
    yearTable = arcpy.CreateTable_management(outputSpace, summaryFile + ".dbf", "", "")
    
    # Adds fields to final table
    arcpy.AddField_management(yearTable, "NAME", "TEXT", "", "", 24, "", "", "", "")
    arcpy.AddField_management(yearTable, "MONTH", "TEXT", "", "", 2, "", "", "", "")
    arcpy.AddField_management(yearTable, "YEAR", "TEXT", "", "", 4, "", "", "", "")
    arcpy.AddField_management(yearTable, "TYPE", "TEXT", "", "", 20, "", "", "", "")    
    arcpy.AddField_management(yearTable, "ZONE_CODE", "LONG", "", "", "", "", "", "", "")
    arcpy.AddField_management(yearTable, "COUNT", "LONG", "", "", "", "", "", "", "")
    arcpy.AddField_management(yearTable, "AREA", "DOUBLE", "", "", "", "", "", "", "")
    arcpy.AddField_management(yearTable, "MIN", "DOUBLE", "", "", "", "", "", "", "")
    arcpy.AddField_management(yearTable, "MAX", "DOUBLE", "", "", "", "", "", "", "")
    arcpy.AddField_management(yearTable, "RANGE", "DOUBLE", "", "", "", "", "", "", "")
    arcpy.AddField_management(yearTable, "MEAN", "DOUBLE", "", "", "", "", "", "", "")
    arcpy.AddField_management(yearTable, "STD", "DOUBLE", "", "", "", "", "", "", "")
    arcpy.AddField_management(yearTable, "SUM", "DOUBLE", "", "", "", "", "", "", "")
    
    # Begins a loop, fetching a list of files from the input workspace and storing them in the variable "CDFs".
    for CDFs in fileList:
    
        # If the file begins with "Fluxes", create rasters and tables for baseflow, evapotranspiration, runoff, and soil moisture.
        # At the time this script was created, files were in the format of "Fluxes_Livneh_NAmerExt_15Oct2014.*four digit year**two digit month*.nc" and
        # "livneh_NAmerExt_15Oct2014.*four digit year**two digit month*.mon.nc".
        if CDFs.startswith("Fluxes"):
        
            # Creates a raster from the netCDF file stored in "CDFs" using the "Baseflow" variable, "lon" as the x-dimension, "lat" as the y-dimension, and default variables for
            # the rest.
            print "Creating baseflow raster for " + CDFs + "..."
            rasterBaseflow = arcpy.MakeNetCDFRasterLayer_md (CDFs, "Baseflow", "lon", "lat", os.path.join(outputSpace, "baseflow"), "", "", "")
            
            # Creates a Zonal Statistics table using the specified zone layer as the zones, the watershed names as the distinguishing fields, the previously created raster as
            # the input raster, and default variables for the rest.
            print "Creating baseflow table for " + CDFs + "...\n"
            outputTable = os.path.join(outputSpace, "baseflow_" + CDFs[37:39] + "_" + CDFs[33:37] + ".dbf")
            arcpy.sa.ZonalStatisticsAsTable (zones, "NAME", rasterBaseflow, outputTable, "", "")
            
            # Adds month, year, and type fields to newly created table.
            arcpy.AddField_management(outputTable, "MONTH", "TEXT", "", "", 2, "", "", "", "")
            arcpy.AddField_management(outputTable, "YEAR", "TEXT", "", "", 4, "", "", "", "")
            arcpy.AddField_management(outputTable, "TYPE", "TEXT", "", "", 20, "", "", "", "")
            
            # Populate month, year, and type fields in new table.
            with arcpy.da.UpdateCursor(outputTable, ["MONTH", "YEAR", "TYPE"], "", "", "", (None, None)) as cursor:
                for row in cursor:
                    row[0] = CDFs[37:39]
                    row[1] = CDFs[33:37]
                    row[2] = "Baseflow"
                    cursor.updateRow(row)
            
            # Appends newly created table to final table.
            arcpy.Append_management(outputTable, yearTable, "NO_TEST", "", "")
            
            # Repeat the above for evapotranspiration.
            print "Creating evapotranspiration raster for " + CDFs + "..."
            rasterTotalET = arcpy.MakeNetCDFRasterLayer_md (CDFs, "TotalET", "lon", "lat", os.path.join(outputSpace, "evapo"), "", "")
            print "Creating evapotranspiration table for " + CDFs + "...\n"
            outputTable = os.path.join(outputSpace, "evapo_" + CDFs[37:39] + "_" + CDFs[33:37] + ".dbf")
            arcpy.sa.ZonalStatisticsAsTable (zones, "NAME", rasterTotalET, outputTable, "", "")

            # Adds month, year, and type fields to newly created table.
            arcpy.AddField_management(outputTable, "MONTH", "TEXT", "", "", 2, "", "", "", "")
            arcpy.AddField_management(outputTable, "YEAR", "TEXT", "", "", 4, "", "", "", "")
            arcpy.AddField_management(outputTable, "TYPE", "TEXT", "", "", 20, "", "", "", "")
            
            # Populate month, year, and type fields in new table.
            with arcpy.da.UpdateCursor(outputTable, ["MONTH", "YEAR", "TYPE"], "", "", "", (None, None)) as cursor:
                for row in cursor:
                    row[0] = CDFs[37:39]
                    row[1] = CDFs[33:37]
                    row[2] = "Evapotranspiration"
                    cursor.updateRow(row)
            
            # Appends newly created table to final table.
            arcpy.Append_management(outputTable, yearTable, "NO_TEST", "", "")
            
            print "Creating runoff raster for " + CDFs + "..."
            rasterRunoff = arcpy.MakeNetCDFRasterLayer_md (CDFs, "Runoff", "lon", "lat", os.path.join(outputSpace, "runoff"), "", "")
            print "Creating runoff table for " + CDFs + "...\n"
            outputTable = os.path.join(outputSpace, "runoff_" + CDFs[37:39] + "_" + CDFs[33:37] + ".dbf")
            arcpy.sa.ZonalStatisticsAsTable (zones, "NAME", rasterRunoff, outputTable, "", "")

            # Adds month, year, and type fields to newly created table.
            arcpy.AddField_management(outputTable, "MONTH", "TEXT", "", "", 2, "", "", "", "")
            arcpy.AddField_management(outputTable, "YEAR", "TEXT", "", "", 4, "", "", "", "")
            arcpy.AddField_management(outputTable, "TYPE", "TEXT", "", "", 20, "", "", "", "")
            
            # Populate month, year, and type fields in new table.
            with arcpy.da.UpdateCursor(outputTable, ["MONTH", "YEAR", "TYPE"], "", "", "", (None, None)) as cursor:
                for row in cursor:
                    row[0] = CDFs[37:39]
                    row[1] = CDFs[33:37]
                    row[2] = "Runoff"
                    cursor.updateRow(row)
            
            # Appends newly created table to final table.
            arcpy.Append_management(outputTable, yearTable, "NO_TEST", "", "")
            
            print "Creating soil moisture raster for " + CDFs + "..."
            rasterSoilMoist = arcpy.MakeNetCDFRasterLayer_md (CDFs, "SoilMoist", "lon", "lat", os.path.join(outputSpace, "soilmoist"), "", "")
            print "Creating soil moisture table for " + CDFs + "...\n"
            outputTable = os.path.join(outputSpace, "soilmoist_" + CDFs[37:39] + "_" + CDFs[33:37] + ".dbf")
            arcpy.sa.ZonalStatisticsAsTable (zones, "NAME", rasterSoilMoist, outputTable, "", "")

            # Adds month, year, and type fields to newly created table.
            arcpy.AddField_management(outputTable, "MONTH", "TEXT", "", "", 2, "", "", "", "")
            arcpy.AddField_management(outputTable, "YEAR", "TEXT", "", "", 4, "", "", "", "")
            arcpy.AddField_management(outputTable, "TYPE", "TEXT", "", "", 20, "", "", "", "")
            
            # Populate month, year, and type fields in new table.
            with arcpy.da.UpdateCursor(outputTable, ["MONTH", "YEAR", "TYPE"], "", "", "", (None, None)) as cursor:
                for row in cursor:
                    row[0] = CDFs[37:39]
                    row[1] = CDFs[33:37]
                    row[2] = "Soil Moisture"
                    cursor.updateRow(row)
            
            # Appends newly created table to final table.
            arcpy.Append_management(outputTable, yearTable, "NO_TEST", "", "")
            
        # If the file begins with anything else, create rasters and tables for precipitation.
        elif CDFs.startswith("livneh"):
            print "Creating precipitation raster for " + CDFs + "..."
            rasterPrecip = arcpy.MakeNetCDFRasterLayer_md (CDFs, "Prec", "lon", "lat", os.path.join(outputSpace, "precip"), "", "")
            print "Creating precipitation table for " + CDFs + "...\n"
            outputTable = os.path.join(outputSpace, "precip_" + CDFs[30:32] + "_" + CDFs[26:30] + ".dbf")
            arcpy.sa.ZonalStatisticsAsTable (zones, "NAME", rasterPrecip, outputTable, "", "ALL")

            # Adds month, year, and type fields to newly created table.
            arcpy.AddField_management(outputTable, "MONTH", "TEXT", "", "", 2, "", "", "", "")
            arcpy.AddField_management(outputTable, "YEAR", "TEXT", "", "", 4, "", "", "", "")
            arcpy.AddField_management(outputTable, "TYPE", "TEXT", "", "", 20, "", "", "", "")
            
            # Populate month, year, and type fields in new table.
            with arcpy.da.UpdateCursor(outputTable, ["MONTH", "YEAR", "TYPE"], "", "", "", (None, None)) as cursor:
                for row in cursor:
                    row[0] = CDFs[30:32]
                    row[1] = CDFs[26:30]
                    row[2] = "Precipitation"
                    cursor.updateRow(row)
            
            # Appends newly created table to final table.
            arcpy.Append_management(outputTable, yearTable, "NO_TEST", "", "")
        else:
            pass
            
    # Returns Spatial Analyst license for use by others.
    arcpy.CheckInExtension("Spatial")
    
    # Converts summary dBASE table to an Excel 2003 table.
    arcpy.TableToExcel_conversion (yearTable, os.path.join(outputSpace, summaryFile + ".xls"), "", "")

    # Deletes dBASE files generated in constructing Excel file.
    outputFiles = os.listdir(outputSpace)
    os.chdir(outputSpace)
    for toDelete in outputFiles:
        if toDelete.endswith(".xls"):
            pass
        elif toDelete.endswith(".lock"):
            pass
        else:
            os.remove(toDelete)
            
    print "Check " + outputSpace + " for the created summary file, " + summaryFile + "."
    # Closes console.
    raw_input("Script completed. Press Enter to quit.")

# Error handling.
except LicenseError:
    print "Spatial Analyst license unavailable."
    
except Exception as e:
    # If an error occurred, print line number and error message
    import traceback, sys
    tb = sys.exc_info()[2]
    print "An error occured on line %i" % tb.tb_lineno
    print str(e)