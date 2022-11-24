"""Module providing operations on files"""
import csv

def openFile(path, writeAccess):
    """Opens a file and returns the file object"""
    if writeAccess:
        file = open(path, "w", encoding="utf-8")
    else:
        file = open(path, "r", encoding="utf-8")

    return file

def getListFromCSV(path):
    """Opens a CSV file and returns a list of lists"""
    if isFileCSV(path):
        file = openFile(path, False)
        reader = csv.reader(file)
        array = list(reader)
        file.close()
    else:
        print("Error: File is not a CSV file")
        array = []

    return array

def isFileCSV(path):
    """Checks if a file is a CSV file"""
    return path.endswith(".csv")

def updateCellInCSV(path, row, column, value):
    """Updates a cell in a CSV file"""
    if isFileCSV(path):
        file = openFile(path, False)
        reader = csv.reader(file)
        array = list(reader)
        file.close()

        array[row][column] = value

        file = openFile(path, True)
        writer = csv.writer(file)
        writer.writerows(array)
        file.close()
    else:
        print("Error: File is not a CSV file")
