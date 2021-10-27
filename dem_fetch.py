# Purpose: a script to download zipped DEMs from URLs in a file for future manipulation.
#
# Version 1.1
#
# Requires: a pre-exisitng file containing URLs. This was made for use on the MnDNR's FTP
# server, so if you'd like to use it on a different server, variables will have to be adjusted.
#---
# MIT License (https://en.wikipedia.org/wiki/MIT_License)
#
# Copyright (c) 2017 Gerrit VanderWaal
#---

print("importing libraries...")
import ftplib
import os
import time
import zipfile

# Creates file object at a given location with read-only permissions ('r')
print("opening URL file...")
url_file = open(r"C:\Users\Gerrit\GIS\optimal_agate_picking\URLs.txt",'r')

# Sets output directory
output_dir = r"C:\Users\Gerrit\GIS\optimal_agate_picking\DEM_zips"

# Opens anonyous connection [login()] to FTP server hosting DEMs
print("connecting to DNR FTP server...")
ftp_server = ftplib.FTP('ftp.lmic.state.mn.us')
ftp_server.login()

# Fetches list (literally) of files from desired directories for later error-proofing
block1_dir = ftp_server.nlst(r"/pub/data/elevation/lidar/projects/arrowhead/block_1/geodatabase")
block3_dir = ftp_server.nlst(r"/pub/data/elevation/lidar/projects/arrowhead/block_3/geodatabase")

count = 0
invalid_url = 0

# Loops through the URLs contained in the local file
for URL in url_file:
  
    # Create new file path to change directories into, also checks against directories
    new_ftp_dir = os.path.join("/pub/data/elevation/lidar/projects/arrowhead/" + URL[71:79] + "geodatabase/")
  
    # Create filename to fetch
    new_ftp_dem = URL[91:].rstrip('\r\n')
  
    # Creates the full filepath on the remote server based on the local URL file
    check_file = os.path.join(new_ftp_dir,new_ftp_dem)
  
    # Checks whether or not the file actually exists. If it does not, the loop iterates.
    if (check_file in block1_dir) or (check_file in block3_dir):
  
        count += 1

        # Sets new local file name
        new_local_dem = os.path.join(output_dir,new_ftp_dem)

        # Change into previously created file path
        ftp_server.cwd(new_ftp_dir)
  
        # Retrieve DEM designated in URL, where the file in newDEM is passed to RETR with the %s placeholder.
		# https://docs.python.org/3.4/library/string.html#string-formatting leads me to believe this may be
		# unecessary but it stays.
        print("fetching " + new_ftp_dem + ", saving to disk...")
        ftp_server.retrbinary('RETR %s' % new_ftp_dem, open(new_local_dem, 'wb').write)

        # Returns to base directory
        ftp_server.cwd('/pub/data/elevation/lidar/projects/arrowhead/')
  
        # Creates a zipfile object, extracts the given file, and closes the object
        print("unzipping...")
        zip_object = zipfile.ZipFile(new_local_dem, 'r')
        zip_object.extractall(output_dir)
        zip_object.close()

        # Waiting 5 seconds before fetching another file, for the sake of politeness
        print("waiting 5 seconds...\n")
        time.sleep(5)

    else:
        invalid_url += 1

print("\n" + str(count) + " valid url(s)")
print(str(invalid_url) + " invalid url(s)\n")

print("deleting downloaded .zip files...)

# Closes FTP connection
print("freeing system resources...")
ftp_server.quit()

# Deletes file object, freeing system resources
url_file.close()