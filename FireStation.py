# Purpose: A script that iterates through a .gdb, creating service areas for given fire
# station points.
#
# Requires: arcpy and os modules, pre-existing geodatabases to take files from and deposit
# into, Network Analyst extension.
#
# Version: 0.9
#
#---
# MIT License (https://en.wikipedia.org/wiki/MIT_License)
#
# Copyright (c) 2017 Gerrit VanderWaal
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#---

print "Importing os module..."
import os

print "Importing arcpy module..."
import arcpy

# Creates custom exception error to be used in case the Spatial Analyst license is unavailable. This section does nothing but is called later.
# in the script if needed. See https://docs.python.org/2.7/tutorial/errors.html for more info.
class LicenseError(Exception):
    pass

# Checks that the Spatial Analyst extension is installed, calls the LicenseError exception if it is not.
print "Checking Network Analyst license..."
if arcpy.CheckExtension("Network") == "Available":
    arcpy.CheckOutExtension("Network")
    print "License retrieved.\n"
else:
    raise LicenseError
    
try:
   
    # Set environment settings
    inputSpace = raw_input("Enter geodatabase containing points as a complete filepath: ")
    arcpy.env.workspace = inputSpace
    
    # Enable data overwriting
    arcpy.env.overwriteOutput = True
    
    # Ask user for the network dataset to be used in this calculation
    networkDataset = raw_input("Enter network dataset for use in script (complete filepath): ")
    
    # Ask user for the output directory
    outputSpace = raw_input("Enter output directory (complete filepath): ")
    
    # Ask user for input points
    print "Listing point classes in geodatabase...\n"
    input = arcpy.ListFeatureClasses()
    
    for newSA in input:
        # Creates the service layer that that locations (fire station points) will be added to.
        # We want lines set at intervals of 5, 10, and 15 minutes, with various other arguments.
        # See http://desktop.arcgis.com/en/arcmap/10.3/tools/network-analyst-toolbox/make-service-area-layer.htm
        # for details.
        print "Creating network service layer..."
        serviceLayer = arcpy.na.MakeServiceAreaLayer(networkDataset, "ServiceArea", "TravelTime", "TRAVEL_FROM", "5 10 15", "NO_POLYS", "", "", "TRUE_LINES", "NON_OVERLAP", "SPLIT", "", "", "ALLOW_UTURNS", ['Avoid Gates','Avoid Private Roads','Driving an Emergency Vehicle','Roads Under Construction Prohibited','Through Traffic Prohibited'], "", "", "NO_LINES_SOURCE_FIELDS", "NO_HIERARCHY", "")
                
        # Get the layer object from the previous result so it can be referenced using the layer object.
        print "Grabbing service layer object..."
        serviceLayer = serviceLayer.getOutput(0)
        
        # Get the names of all sublayers within the service area layer
        print "Grabbing names of sublayers within service layer object..."
        subLayerNames = arcpy.na.GetNAClassNames(serviceLayer)
        
        # Stores the layer names for later use.
        print "Storing sublayers for later use..."
        facilitiesNames = subLayerNames["Facilities"]
        lineData = subLayerNames["SALines"]
        lineSubLayer = arcpy.mapping.ListLayers(serviceLayer, lineData)[0] # Complete file path needs to be listed to use CopyFeatures_management. CF_m does not know full path (*layer_name*\*sublayer*) if only lineData is used
        
        # Load fire station locations using the service layer object, sublayers of that object, the fire station inputs, and default other settings.
        print "Loading fire station locations..."
        arcpy.na.AddLocations(serviceLayer, facilitiesNames, newSA, "", "", "", "", "", "", "", "", "", "")
        
        # Solve network analysis problem.
        print "Solving network analysis problem..."
        arcpy.na.Solve(serviceLayer, "", "", "")
        
        #Save the solved output to a feature class using the spatial reference of the input feature class. SEE: https://geonet.esri.com/thread/170943
        print "Saving to .lyr..."
        layer = arcpy.management.SaveToLayerFile(serviceLayer, os.path.join(outputSpace, newSA[0:7] + ".lyr"), "RELATIVE") # uses first 8 characters of file in newSA cuz who knows what the file names are gonna be like
        print "Saving to feature class..."
        arcpy.CopyFeatures_management(lineSubLayer, os.path.join(outputSpace, newSA[0:7]), "", "", "", "")

    print "Script complete."
    
except LicenseError:
    print "Spatial Analyst license unavailable."
    
except Exception as e:
    # If an error occurred, print line number and error message
    import traceback, sys
    tb = sys.exc_info()[2]
    print "An error occured on line %i" % tb.tb_lineno
    print str(e)
