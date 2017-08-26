# Purpose: a script to download zipped DEMs from URLs in a file for future manipulation.
#
# Version 0.3
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
import ftplib
import os

# Creates file object at a given location with read-only permissions ('r')
URLfile = open(r"C:\Users\Gerrit\GIS\optimal_agate_picking\URLs.txt",'r')

# Sets output directory
outputDir = r"C:\Users\Gerrit\GIS\optimal_agate_picking\DEM_zips"

# Opens anonyous connection [login()] to FTP server hosting DEMs
FTPserver = FTP('ftp.lmic.state.mn.us')
FTPserver.login()

# Loops through the URLs contained in the file
for URL in URLfile:
  # Create new filepath to change directories into
  newDir = os.path.join("pub/data/elevation/lidar/projects/arrowhead/" + URL[71:79] + "geodatabase/")
  
  # Create filename to fetch
  newDEM = URL[91:]
  
  # Change into previously created directory
  FTPserver.cwd(newDir)
  
  # Retrieve DEM designated in URL, where the file in newDEM is passed to RETR with the %s placeholder.
  #
  #
  FTPserver.retrbinary('RETR %s' % newDEM, open(os.path.join(outputDir,newDEM), 'wb').write()) #check whether or not the os.path.join works, or if this even saves stuff
  #
  #
  #
  
  print(newDir)
  print(newDEM)

# Closes FTP connection
FTPserver.quit()
# Deletes file object, freeing system resources
URLfile.close()
