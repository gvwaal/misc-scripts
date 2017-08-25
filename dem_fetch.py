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

# Creates file object at a given location with only read permissions ('r')
URLfile = open(r"C:\Users\Gerrit\GIS\optimal_agate_picking\URLs.txt",'r')

# Loops through the URLs contained in the file, fetching the DEM from each one
for URL in URLfile:
  # FETCH THINGS FROM THE URL
  print(URL)

# Deletes file object, freeing system resources
URLfile.close()
