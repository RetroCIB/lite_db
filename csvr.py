#! /usr/bin/python 
#

import csv
import sys
import os

#print  *.csv files with listdir
def csv_contents(sPath):
    dir_a = os.listdir(sPath)
    csv_dir = [i for i in dir_a if ".csv" in i]
    return csv_dir

#raw_input .csv file name
def _input(msg):
    return raw_input (msg)

# Open csv file and  get a ows
def file_names(filename):
    print "Start reading file : ", filename
    with open(filename, 'rb') as f:
        reader = csv.reader(f)
        try:
            for row in reader:
                break
        except csv.Error as e:
            sys.exit('file %s, line %d: %s' % (filename, reader.line_num, e))
    return row

#main function
def main():
    sDir = csv_contents(".")
    print "Enter the name of CSV file: ****.csv : "
    sDir = _input(sDir)
    if os.path.isfile(sDir):
        print "File has been found : ", sDir
    else:
        sys.exit('File does not exist: %s' %(sDir))
    row = file_names(sDir)
    print "First row ", row
    print "Length :", len(row)


main()
