"""Module providing operations on files"""
import csv

def io_openFile(path, writeAccess):
    """Opens a file and returns the file object"""
    if writeAccess:
        file = open(path, "w", encoding="utf-8")
    else:
        file = open(path, "r", encoding="utf-8")

    return file

def io_getListFromCSV(path):
    """Opens a CSV file and returns a list of lists"""
    file = io_openFile(path, False)
    reader = csv.reader(file)
    array = list(reader)
    file.close()
    return array
