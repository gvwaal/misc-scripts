# Script for converting the MPCA's Lab_MN EDD format to EQEDD for upload to
# EQuIS. On occasion, some labs are only able to provide Lab_MNs, and a
# script does the conversion more quickly than a human cutting and pasting
# columns around in Excel.
#
# Script assumptions:
#   1. Script is being run with Python 3.6 on Windows 10. Script was created
#      with Python 3.6.0 on Windows 10 Pro 21H1.
#   2. User provides a directory which contains either one Lab_MN .zip file,
#      or three delimited text files with certain strings in the file name.
#   3. The Lab_MN and EQEDD contain the same set of fields as what was
#      referenced when the script was created. The user will see whether this
#      is true based on how EDP responds when the EQEDD is loaded. If the set
#      of fields has changed, the user may need to tweak the script.
#
# Future to-do:
#   - XML parsing to accept an .xlsx as an input, since that's how the MDH
#     delivers Lab_MNs
#
# MIT License (https://en.wikipedia.org/wiki/MIT_License)
#
# Copyright (c) 2021 Gerrit VanderWaal
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

import os
import csv
from zipfile import ZipFile
import tempfile

# Section within the pound signs are dictionaries containing the values in the
# Lab_MN and the corresponding destination reference value. In some cases these
# are incomplete by design - for example, it would be inadvisable to include
# all Lab_MN lab_anl_method_names since the company uses MDH for select
# analyses. The user will need to add methods when necessary.
#######################################
#######################################
# sample_type_codes containing "NCS" appear to be the equivalent of non-site
# samples and are discarded when the sample_parser() function checks for rows
# with empty field_sdg values.
sample_type_code = {'sample_type_code': 'sample_type_code',
                    'Sample': 'dest_ref_val',
                    'QC-FR': 'dest_ref_val',
                    'QC-EB': 'dest_ref_val',
                    'QC-FB': 'dest_ref_val',
                    'QC-TB': 'dest_ref_val',
                    'QC-LB': 'dest_ref_val',
                    'QC-LS': 'dest_ref_val',
                    'QC-LSD': 'dest_ref_val',
                    'QC-LMS': 'dest_ref_val',
                    'QC-LMSD': 'dest_ref_val',
                    'QC-LD': 'dest_ref_val'}

# Lab_MN values are lowercase to account for inconsistent capitalization
# between labs. This reduces the probability of failure in sample_parser().
sample_matrix_code = {'sample_matrix_code': 'sample_matrix_code',
                      'drinking water': 'dest_ref_val',
                      'wtr-drink': 'dest_ref_val',
                      'wtr-ground': 'dest_ref_val',
                      'qc-blank': 'dest_ref_val'}

lab_anl_method_name = {'lab_anl_method_name': 'lab_anl_method_name',
                       '524.3': 'dest_ref_val',
                       '533': 'dest_ref_val',
                       'MDH522': 'dest_ref_val',
                       'AXYS_MLA-110 ': 'dest_ref_val',
                       '900': 'dest_ref_val',
                       'MDH555': 'dest_ref_val'}

total_or_dissolved = {'total_or_dissolved': 'total_or_dissolved',
                      'Total': 'dest_ref_val',
                      'Dissolved': 'dest_ref_val'}
#######################################
#######################################


def sample_parser(mdh_labsample, dest_labsample, samples_to_skip):
    '''Function to parse the Lab_MN LabSample_v1 file.

    1. Takes in the input LabSample, the file path for the output LabSample,
    and an empty list to contain samples to skip.
    2. Parses the file to populate the list of samples to skip and creates the
    output LabSample file in a temporary directory.
    3. Returns the SDG# for use in results_parser().
    '''
    # Opens the Lab_MN LabSample file and output LabSample file, implemented
    # from this stackoverflow post:
    # https://stackoverflow.com/a/57518881
    with open(mdh_labsample, newline='') as input_file, open(dest_labsample, 'w', newline='') as output_file:
        
        # In some cases, the first row of the file will be the header, so to
        # give csv.Sniffer() a representative sample, skips twice to the third
        # row. In rarer cases, it's possible the second row could be a
        # description of the field.
        next(input_file)
        next(input_file)

        # Automatically detects the "dialect" of the file. The dialect are
        # things like delimiter character and quoting preference. This is done
        # to avoid having the user specify what the character delimiter is and
        # having to implement more lines to deal with that input. It assumes
        # the script will only encounter comma- and tab-delimited files, but
        # the user will need to tweak accordingly if they receive files
        # delimited otherwise.
        # https://docs.python.org/3.6/library/csv.html#csv.Sniffer
        dialect = csv.Sniffer().sniff(input_file.readline(), [',', '\t'])
        input_file.seek(0)

        # Assigns the returned reader object to a variable using the dialect
        # detected above. The same occurrs with the writing file but with
        # specified dialect settings.
        reader = csv.reader(input_file, dialect)
        writer = csv.writer(output_file, delimiter='\t',
                            quotechar='"', quoting=csv.QUOTE_MINIMAL)

        # Iterates through the input file loaded in the reader object.
        for row in reader:

            # If the SDG# is blank or the sample type is QC-O, skip the row.
            # In the context in which this script was designed, "non-site",
            # or samples that are not from the SDG being processed, aren't
            # uploaded to EQuIS and are skipped.
            if row[7] == '' or row[4] == 'QC-O':
                # Appends the undesired sample's sys_sample_code to
                # samples_to_skip so they can be skipped in later functions.
                samples_to_skip.append(row[0])
                pass
            else:
                # Sets the SDG# for reference in results_parser().
                field_sdg = row[7]

                # Sets the value for sampling_company_code under the
                # assumption the script is parsing an MDH Lab_MN. This isn't
                # necessarily the case since other labs can provide Lab_MNs,
                # but this is relatively uncommon.
                if row[5] == 'Field':
                    sampling_company_code = 'dest_comp_code'
                else:
                    sampling_company_code = 'dest_ref_for_MDH'
                
                # Writes the output row. lower() is used so referencing the
                # dictionary doesn't break.
                writer.writerow([row[0], row[0],
                                 sample_matrix_code[row[3].lower()],
                                 sample_type_code[row[4]], row[5], row[6],
                                 row[7], row[8] + '  ' + row[9], '', '', '',
                                 '', '', '', '', row[20],
                                 sampling_company_code])

    return field_sdg


def results_parser(mdh_testresultsqc, dest_testresultsqc,
                   samples_to_skip, field_sdg):
    '''Function to parse the Lab_MN TestResultsQC_v1 file.

    1. Takes in the input TestResultsQC, the file path for the output
    TestResultsQC, an empty list to contain samples to skip, and the SDG#
    identified in sample_parser().
    2. Parses the file to change various values and creates the output
    TestResultsQC file in a temporary directory.
    '''
    # Opens the Lab_MN TestResultsQC file and output TestResultsQC file,
    # implemented from this stackoverflow post:
    # https://stackoverflow.com/a/57518881
    with open(mdh_testresultsqc, newline='') as input_file, open(dest_testresultsqc, 'w', newline='') as output_file:
        
        # In some cases, the first row of the file will be the header, so to
        # give csv.Sniffer() a representative sample, skips twice to the third
        # row. In rarer cases, it's possible the second row could be a
        # description of the field.
        next(input_file)
        next(input_file)

        # Automatically detects the "dialect" of the file. The dialect are
        # things like delimiter character and quoting preference. This is done
        # to avoid having the user specify what the character delimiter is and
        # having to implement more lines to deal with that input. It assumes
        # the script will only encounter comma- and tab-delimited files, but
        # the user will need to tweak accordingly if they receive files
        # delimited otherwise.
        # https://docs.python.org/3.6/library/csv.html#csv.Sniffer
        dialect = csv.Sniffer().sniff(input_file.readline(), [',', '\t'])
        input_file.seek(0)

        # Assigns the returned reader object to a variable using the dialect
        # detected above. The same occurrs with the writing file but with
        # specified dialect settings.
        reader = csv.reader(input_file, dialect)
        writer = csv.writer(output_file, delimiter='\t',
                            quotechar='"', quoting=csv.QUOTE_MINIMAL)

        # Iterates through the input file loaded in the reader object.
        for row in reader:

            # If the sys_sample_code is present in the list of samples to
            # skip, skip the row.
            if row[0] in samples_to_skip:
                pass
            else:
                # If the prep method is listed as "Unspecified", assume the
                # prep method is just the lab_anl_method_name, otherwise use
                # whatever's in lab_prep_method for the output.
                if row[21] == 'Unspecified':
                    lab_prep_method = 'METHOD'
                else:
                    lab_prep_method = row[21]
                
                # If the lab qualifier contains a <, replace it with a U,
                # since that's what was used for non=detects.
                if '<' in row[47]:
                    lab_qualifiers = row[47].replace('<', 'U')
                else:
                    lab_qualifiers = row[47]
                
                # Writes the output row.
                writer.writerow([row[0], lab_anl_method_name[row[1]], row[2],
                                 total_or_dissolved[row[3]], row[4], row[5],
                                 'WQ', 'LB', 'Wet', row[27], row[20],
                                 lab_prep_method, row[22], '', '',
                                 'dest_ref_for_MDH', row[26], row[27], row[28],
                                 '', '', row[31], row[32], '', '', '', '',
                                 row[36], row[37], row[39], '', row[43], 'Yes',
                                 row[45], lab_qualifiers, '', lab_qualifiers,
                                 '', row[48], row[49], row[49], row[50],
                                 row[50], '', '', field_sdg, row[56], row[57],
                                 row[58], row[59], row[60], row[61], row[62],
                                 row[63], row[64], row[65], row[66], row[67],
                                 row[68], row[69], row[70]])


def batch_parser(mdh_testbatch, dest_testbatch, samples_to_skip):
    '''Function to parse the Lab_MN TestBatch_v1 file.

    1. Takes in the input TestBatch, the file path for the output TestBatch,
    and an empty list to contain samples to skip.
    2. Parses the file to change various values and creates the output
    TestBatch file in a temporary directory.
    '''
    # Opens the Lab_MN TestBatch file and output TestBatch file, implemented
    # from this stackoverflow post:
    # https://stackoverflow.com/a/57518881
    with open(mdh_testbatch, newline='') as input_file, open(dest_testbatch, 'w', newline='') as output_file:

        # In some cases, the first row of the file will be the header, so to
        # give csv.Sniffer() a representative sample, skips twice to the third
        # row. In rarer cases, it's possible the second row could be a
        # description of the field.        
        next(input_file)
        next(input_file)

        # Automatically detects the "dialect" of the file. The dialect are
        # things like delimiter character and quoting preference. This is done
        # to avoid having the user specify what the character delimiter is and
        # having to implement more lines to deal with that input. It assumes
        # the script will only encounter comma- and tab-delimited files, but
        # the user will need to tweak accordingly if they receive files
        # delimited otherwise.
        # https://docs.python.org/3.6/library/csv.html#csv.Sniffer
        dialect = csv.Sniffer().sniff(input_file.readline(), [',', '\t'])
        input_file.seek(0)

        # Assigns the returned reader object to a variable using the dialect
        # detected above. The same occurrs with the writing file but with
        # specified dialect settings.        
        reader = csv.reader(input_file, dialect)
        writer = csv.writer(output_file, delimiter='\t',
                            quotechar='"', quoting=csv.QUOTE_MINIMAL)
        
        # Iterates through the input file loaded in the reader object.
        for row in reader:

            # If the sys_sample_code is present in the list of samples to
            # skip, skip the row.
            if row[0] in samples_to_skip:
                pass
            else:
                # Writes the output row.
                writer.writerow([row[0], lab_anl_method_name[row[1]], row[2],
                                 total_or_dissolved[row[3]], row[4], row[5],
                                 'Analysis', row[9]])


#file_path = input('Paste/type the full file path (e.g. C:\\workspace\\a_folder) for the folder\ncontaining a Lab_MN to convert to EQEDD, then hit Enter. The Lab_MN can be\npresent as either:\n\t1. One .zip file whose contents are at least three comma- or\n\ttab-delimited files with file names containing the strings "labsample",\n\t"testresultsqc", and "testbatch" (case insensitive)\n\t-or-\n\t2. Three comma- or tab-delimited files whose file names contain\n\tthose strings.\n\nIf both are present the text files will be skipped.\n')
file_path = r'C:\workspace\LabMN2EQEDD'

# These two bits of information are passed around differently. Implementing
# field_sdg in a similar manner to samples_to_skip results in writing brackets
# to the lab_sdg field in TestResultsQC. So somehow, samples_to_skip can be
# populated in the sample_parser function and not be returned but is still
# accessible to the other functions, but field_sdg needs to be returned and
# passed back into the other function. Unclear why this happens.
samples_to_skip = []
field_sdg = []

# Creates a temporary directory to do the interstitial file saving in.
# Eliminates the need to specify a working/scratch directory by the user, and
# avoids cluttering up the directory provided by the user. When all the sample
# parsing and EQEDD creation is complete, deletes the temporary directory and
# contents.
# https://docs.python.org/3.6/library/tempfile.html#tempfile.TemporaryDirectory
with tempfile.TemporaryDirectory() as temp_dir:

    # Lists the files in the directory provided by the user, then iterates
    # through them.
    for files in os.listdir(file_path):

        # If the Lab_MN is provided by the user as a .zip, proceed with one
        # way of saving the files.
        if '.zip' in files:

            # Extract files from the .zip to the temporary directory for
            # parsing.
            with ZipFile(files, 'r') as edd_zip:
                edd_zip.extractall(temp_dir)
            
            # Lists the files extracted into the temporary directory and
            # iterates through them.
            for unzipped_file in os.listdir(temp_dir):

                # If various strings are present in the file names, assign
                # them to variables for parsing. lower() is used to aid string
                # comparison.
                if 'labsample' in unzipped_file.lower():
                    mdh_labsample = os.path.join(temp_dir, unzipped_file)
                elif 'testresultsqc' in unzipped_file.lower():
                    mdh_testresultsqc = os.path.join(temp_dir, unzipped_file)
                elif 'testbatch' in unzipped_file.lower():
                    mdh_testbatch = os.path.join(temp_dir, unzipped_file)
        
        # If the Lab_MN is provided as standalone files, checks for various
        # strings in the file names and assigns them to variables for parsing.
        # lower() is used to aid string comparison.
        elif 'labsample' in files.lower():
            mdh_labsample = os.path.join(file_path, files)
        elif 'testresultsqc' in files.lower():
            mdh_testresultsqc = os.path.join(file_path, files)
        elif 'testbatch' in files.lower():
            mdh_testbatch = os.path.join(file_path, files)

    # Variables containing the output file names.
    dest_labsample = os.path.join(temp_dir, 'out.LabSample_v1.txt')
    dest_testresultsqc = os.path.join(temp_dir, 'out.TestResultsQC_v1.txt')
    dest_testbatch = os.path.join(temp_dir, 'out.TestBatch_v1.txt')

    # Calls the functions that do the file parsing/creation.
    field_sdg = sample_parser(mdh_labsample, dest_labsample, samples_to_skip)
    results_parser(mdh_testresultsqc, dest_testresultsqc,
                   samples_to_skip, field_sdg)
    batch_parser(mdh_testbatch, dest_testbatch, samples_to_skip)

    # Creates the output EQEDD .zip file and writes the output files to it.
    with ZipFile(os.path.join(file_path, str(field_sdg) + '.EQEDD.zip'), 'x') as new_zip:
        new_zip.write(dest_labsample, os.path.basename(dest_labsample))
        new_zip.write(dest_testresultsqc, os.path.basename(dest_testresultsqc))
        new_zip.write(dest_testbatch, os.path.basename(dest_testbatch))
