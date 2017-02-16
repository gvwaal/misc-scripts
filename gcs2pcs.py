# Purpose: A script to iterate through a geodatabase, converting the current geographic coordinate
# system for a feature class to a desired projected coordinate system.
#
# Requires: arcpy and os modules, pre-existing geodatabases to take files from and deposit
# into, input files in a geographic information system, and a projected coordinate system
# known to ArcGIS.
#
# Version: 1.0
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

# Import os module
print "Importing os module..."
import os

# Import arcpy module
print "Importing arcpy module..."
import arcpy

try:
    # Ask user for input workspace.
    inputSpace = raw_input("Enter input geodatabase as a complete filepath: ")
    arcpy.env.workspace = inputSpace
    print "Input workspace set to: " + arcpy.env.workspace
    
    # Ask user for output workspace.
    outputSpace = raw_input("Enter output geodatabase as a complete filepath: ")
    print "Output workspace set to: " + outputSpace
    
    # Ask user for new projected coordinate system.
    newProj = raw_input("Enter a projected coordinate system known to ArcGIS as a full name with spaces, a filepath to a .proj file, or factory/authority code: ")
    print newProj
    outPCS = arcpy.SpatialReference(newProj)
    print "Input success."
    
    # Enable data overwriting.
    arcpy.env.overwriteOutput = True
    
    # List the feature classes in the above .gdb and assign them to a variable.
    print "Listing feature classes in geodatabase...\n"
    classes = arcpy.ListFeatureClasses()

    # loop through .gdb, converting current geographic coordinate system to desired coordinate system
    print "Beginning conversion process..."
    for newPCS in classes:
        # Name generated using the output workspace and the current iteration with "_proj" tacked onto the end.
        print "Generating new output file name..."
        output = os.path.join(outputSpace, newPCS + "_proj")
        print "New output file is " + output
        
        # Applies new projected coordinate system to current iteration.
        print "Defining new coordinate system..."
        arcpy.Project_management(newPCS, output, outPCS, "", "", "", "", "")
        print "Definition succeeded.\n"
        
    print "Script complete."
    
# Error handling.
except Exception as e:
    # If an error occurred, print line number and error message.
    import traceback, sys
    tb = sys.exc_info()[2]
    print "An error occured on line %i" % tb.tb_lineno
    print str(e)
