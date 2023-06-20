# This module handles direct interaction with the files of the file sync program


# Import general packages
from __future__ import absolute_import
from datetime import datetime

# Import project files
import comms.file

class FileManager():
    def __init__(self, installPath, managerName):
        self.rootPath = ""
        self.installLocation = installPath
        self.managerName = managerName
        self.allFiles = []
        self.deletedFiles = []

    def getRootPath(self):
        return self.rootPath

    def setRootPath(self, path):
        self.rootPath = path
        self.allFiles = []

    def areFilesPresent(self):
        return len(self.allFiles) > 0

    def discoverFiles(self):
        print("File Manager " + str(self.rootPath) + " Collecting files")
        fileNames = comms.file.getFilesInDirectory(self.rootPath)
        for file in fileNames:
            relativePath = comms.file.getRelativePath(file, self.rootPath)
            self.allFiles.append(FileInfo(file, relativePath))
            print("Discovered " + relativePath)

    def compareAgainstLocalSave(self):
        print("Comparing against saved files from last run")
        loadSavedPath = comms.file.concatenatePaths(self.installLocation, self.managerName + "SavedFiles")
        loadDeletedPath = comms.file.concatenatePaths(self.installLocation, self.managerName + "DeletedFiles")

        previousFiles = comms.file.loadDataFromPickleFile(loadSavedPath)
        self.deletedFiles = comms.file.loadDataFromPickleFile(loadDeletedPath)

        missingFiles = self.compareFiles(previousFiles)

        deletedFilesUpdateNeeded = False
        for missingFile in missingFiles:
            self.deletedFiles.append(DeletedFile(missingFile))
            deletedFilesUpdateNeeded = True

        if deletedFilesUpdateNeeded:
            self.saveFiles("DeletedFiles", self.deletedFiles)

        self.saveFiles("SavedFiles", self.allFiles) # This could be done better but works for now


        # Load saved files from last run.
        # If there is a file missing in the current set vs the last set
            # add that file metadata to deletedFiles list as well as the timestamp when it was removed

        # After the first compare files run, send the list of deleted items
        # if a deleted item match is found then compare the last modified timestamp and the deleted timestamp
        # if the deleted timestamp is greater then delete the file from the system and add it to it's own deleted files list
        # otherwise, send a command to the host that the deleted item needs to be removed from the list as the remote has a more recent copy



    def saveFiles(self, secondPartOfName, data):
        filename = self.managerName + secondPartOfName
        comms.file.storeDataAsPickleFile(self.installLocation, filename, data)

    def getDeletedFiles(self):
        self.compareAgainstLocalSave() # Make sure it's up to date. TODO: This should probably be moved somewhere else
        return self.deletedFiles

    def compareFiles(self, receivedFiles):
        # Returns a list of files that need to be sent from remote
        print("Comparing Files")
        requestedFiles = []
        for receivedFile in receivedFiles:
            fileFound = False
            for savedFile in self.allFiles:
                if receivedFile.getRelativePath() == savedFile.getRelativePath():
                    fileFound = True
                    if not savedFile.isFileNewestCopy(receivedFile):
                        requestedFiles.append(receivedFile)
                        print(receivedFile.getRelativePath() + " remote copy is newer")
                    else:
                        print(receivedFile.getRelativePath() + " local copy is newer or the same")

                    break

            if fileFound == False:
                print(receivedFile.getRelativePath() + " not found")
                requestedFiles.append(receivedFile)

        return requestedFiles

    def getAllFiles(self):
        return self.allFiles

    def getAbsolutePath(self, relativePath):
        return self.rootPath + relativePath

class FileInfo():
    def __init__(self, absolutePath, relativePath):
        self.absolutePath = absolutePath
        self.relativePath = relativePath
        self.fileSize, self.creationTime, self.lastModifiedTime, self.lastAccessedTime = comms.file.extractMetadata(absolutePath)

    def getAbsolutePath(self):
        return self.absolutePath

    def getRelativePath(self):
        return self.relativePath

    def getLastModifiedTime(self):
        return self.lastModifiedTime

    def getFileSize(self):
        return self.fileSize

    def getCreationTime(self):
        return self.creationTime

    def getLastAccessedTime(self):
        return self.lastAccessedTime

    def areFilesTheSame(self, otherFile):
        return (
            self.lastModifiedTime == otherFile.getLastModifiedTime()
            and self.fileSize == otherFile.getFileSize()
            and self.creationTime == otherFile.getCreationTime()
        )

    def isFileNewestCopy(self, otherFile):
        # Returns True if this file is the newest, false otherwise
        if self.lastModifiedTime == otherFile.getLastModifiedTime():
            # This should almost never happen, but if it does then take the file with higher size to avoid losing data
            if self.fileSize == otherFile.getFileSize():
                return True
            else:
                return self.fileSize > otherFile.getFileSize()
        else:
            return self.lastModifiedTime > otherFile.getLastModifiedTime()

class DeletedFile(FileInfo):
    def __init__(self, existingFile):
        super().__init__(existingFile.getAbsolutePath(), existingFile.getRelativePath())
        self.deletedTime = datetime.now()
