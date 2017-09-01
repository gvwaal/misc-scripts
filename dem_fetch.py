# Purpose: a script to download zipped DEMs from URLs in a file for future manipulation.
#
# Version 0.9
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

import zipfile

# Creates file object at a given location with read-only permissions ('r')
print("opening URL file...\n")
url_file = open(r"C:\Users\Gerrit\GIS\optimal_agate_picking\URLs.txt",'r')

# Sets output directory
output_dir = r"C:\Users\Gerrit\GIS\optimal_agate_picking\DEM_zips"

# Opens anonyous connection [login()] to FTP server hosting DEMs
print("connecting to DNR FTP server...")
ftp_server = ftplib.FTP('ftp.lmic.state.mn.us')
ftp_server.login()

# Loops through the URLs contained in the file
for URL in url_file:
  # Create new file path to change directories into
  new_ftp_dir = os.path.join("pub/data/elevation/lidar/projects/arrowhead/" + URL[71:79] + "geodatabase/")
  
  # Create filename to fetch
  new_DEM = URL[91:].rstrip('\r\n')
  print(new_DEM)

  # Sets new local file name
  new_local = os.path.join(output_dir,new_DEM)
  
  # Change into previously created file path
  print("changing into correct remote directory...")
  ftp_server.cwd(new_ftp_dir)

  # Retrieve DEM designated in URL, where the file in newDEM is passed to RETR with the %s placeholder.
  print("fetching " + new_DEM + ", saving to disk...")
  ftp_server.retrbinary('RETR %s' % new_DEM, open(new_local, 'wb').write)
  
  # Unzips retrieved file
  print("unzipping...")
  zip_object = zipfile.ZipFile(new_local, 'r')
  zip_object.extractall(output_dir)
  zip_object.close()
  
  # Waiting 60 seconds before fetching another file, for the sake of politeness
  print("waiting 10 seconds...\n")
  time.sleep(10)

# Closes FTP connection
print("closing FTP connection...")
ftp_server.quit()

# Deletes file object, freeing system resources
print("closing URL file...\n")
url_file.close()
