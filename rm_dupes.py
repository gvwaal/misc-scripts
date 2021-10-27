# Script to remove dupilicate images Google Photos/Drive creates when backing up
# my phone's images. Current record is 288 dupes from 2016.
import os

directory = input("Enter directory to clean: ")

file_list = os.listdir(directory)

del_files = 0

# Initiates 'for' loop to cycle through image files stored in file_list
for files in file_list:
    print(files)
    # If there's a ) right before the file extension and the file extension is
    # only three characters, delete it and keep track of how many are deleted
    if files[-5] == ")":
        del_files += 1
        os.remove(os.path.join(directory, files))

print(str(del_files) + " files deleted")
