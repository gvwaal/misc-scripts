# Purpose: a script to download zipped DEMs from URLs in a file for future manipulation.
#
#
# Requires: a pre-exisitng file containing URLs
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
print("importing ftplib...")
import ftplib

print("importing os...")
import os

print("importing time...\n")
import time

# Creates file object at a given location with read-only permissions ('r')
print("opening URL file...\n")
URLfile = open(r"C:\Users\Gerrit\GIS\optimal_agate_picking\URLs.txt",'r')

# Sets output directory
print("setting output directory...\n")
outputDir = r"C:\Users\Gerrit\GIS\optimal_agate_picking\DEM_zips"

# Opens anonyous connection [login()] to FTP server hosting DEMs
print("connecting to DNR FTP server...")
FTPserver = ftplib.FTP('ftp.lmic.state.mn.us')
FTPserver.login()

# Loops through the URLs contained in the file
for URL in URLfile:
  # Create new file path to change directories into
  newDir = os.path.join("pub/data/elevation/lidar/projects/arrowhead/" + URL[71:79] + "geodatabase/")
  
  # Create filename to fetch
  newDEM = URL[91:]
  
  # Change into previously created file path
  print("changing into proper directory...")
  FTPserver.cwd(newDir)
  
  # Retrieve DEM designated in URL, where the file in newDEM is passed to RETR with the %s placeholder.
  print("fetching " + newDEM + ", saving to disk...")
  FTPserver.retrbinary('RETR %s' % newDEM, open(os.path.join(outputDir,newDEM), 'wb').write) #what kind of argument does write need ?_?
  
  print(newDir)
  print(newDEM)
  
  # Waiting 60 seconds before fetching another file, for the sake of politeness

# Closes FTP connection
FTPserver.quit()

# Deletes file object, freeing system resources
print("closing URL file...\n")
URLfile.close()
