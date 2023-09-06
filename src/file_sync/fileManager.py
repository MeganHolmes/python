# This module handles direct interaction with the files of the file sync program


# Import general packages
from __future__ import absolute_import
from datetime import datetime

# Import project files
import IO.file

class FileManager():
    def __init__(self, installPath, managerName):
        self.rootPath = ""
        self.installLocation = installPath
        self.managerName = managerName
        self.allFiles = []
        self.deletedFiles = []

    def reset(self):
        self.allFiles = []
        self.deletedFiles = []

    def getRootPath(self):
        return self.rootPath

    def setRootPath(self, path):
        self.rootPath = path
        self.allFiles = []

    def areFilesPresent(self):
        return len(self.allFiles) > 0

    def getAllFiles(self):
        return self.allFiles

    def getAbsolutePath(self, relativePath):
        return self.rootPath + relativePath

    def getDeletedFiles(self):
        return self.deletedFiles

    def saveData(self):
        self.saveFile("DeletedFiles", self.deletedFiles)
        self.saveFile("SavedFiles", self.allFiles)

    def saveFile(self, secondPartOfName, data):
        filename = self.managerName + secondPartOfName
        IO.file.storeDataAsPickleFile(self.installLocation, filename, data)

    def deleteFile(self, secondPartOfName):
        filename = self.managerName + secondPartOfName
        IO.file.deletePickleFile(IO.file.concatenatePaths(self.installLocation, filename))

    def deleteSavedData(self):
        self.deleteFile("DeletedFiles")
        self.deleteFile("SavedFiles")

    def discoverFiles(self):
        print("File Manager " + str(self.rootPath) + " Collecting files")
        fileNames = IO.file.getFilesInDirectory(self.rootPath)
        for file in fileNames:
            relativePath = IO.file.getRelativePath(file, self.rootPath)
            self.allFiles.append(FileInfo(file, relativePath))
            print("Discovered " + relativePath)

    def compareAgainstLocalSave(self):
        print("Comparing against saved files from last run")
        loadSavedPath = IO.file.concatenatePaths(self.installLocation, self.managerName + "SavedFiles")
        loadDeletedPath = IO.file.concatenatePaths(self.installLocation, self.managerName + "DeletedFiles")

        previousFiles = IO.file.loadDataFromPickleFile(loadSavedPath)
        self.deletedFiles = IO.file.loadDataFromPickleFile(loadDeletedPath)

        missingFiles = self.compareFiles(previousFiles)

        for missingFile in missingFiles:
            self.deletedFiles.append(DeletedFile(missingFile))
            print("Missing File: " + missingFile.getRelativePath())


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

    def clearDeletedFiles(self, deletedFiles):
        # Remove files that have been deleted from the list
        updateRequired = False
        removeDeletedFiles = []
        for deletedFile in deletedFiles:
            for savedFile in self.allFiles:
                if deletedFile.getRelativePath() == savedFile.getRelativePath():
                    # If we get here then the files match.
                    if deletedFile.isFileNewestCopy(savedFile):
                        # The remote file is newer, so we need to delete the local file
                        print("Deleting " + savedFile.getRelativePath())
                        IO.file.deleteFile(savedFile.getAbsolutePath())
                        self.allFiles.remove(savedFile)
                        updateRequired = True
                    else:
                        # The local file is newer, so we need to remove the file from the deletion list
                        print("Removing " + deletedFile.getRelativePath() + " from deletion list")
                        removeDeletedFiles.append(deletedFile)
                    break

        return updateRequired, removeDeletedFiles

    def removeDeletedFiles(self, remoteDeletedFiles):
        for remoteFile in remoteDeletedFiles:
            for localDeletedFile in self.deletedFiles:
                if remoteFile.getRelativePath() == localDeletedFile.getRelativePath():
                    self.deletedFiles.remove(localDeletedFile)
                    break


class FileInfo():
    def __init__(self, absolutePath, relativePath):
        self.absolutePath = absolutePath
        self.relativePath = relativePath
        self.fileSize, self.creationTime, self.lastModifiedTime, self.lastAccessedTime = IO.file.extractMetadata(absolutePath)

    def __getstate__(self):
        # Return the entire object dictionary for serialization
        return self.__dict__

    def __setstate__(self, state):
        # Update the object's dictionary with the serialized state
        self.__dict__.update(state)

    def __str__(self):
        return f"CustomFileInfo: {self.absolutePath}, {self.relativePath}, {self.fileSize}, {self.creationTime}, {self.lastModifiedTime}, {self.lastAccessedTime}"


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
            self.relativePath == otherFile.getRelativePath()
            and self.lastModifiedTime == otherFile.getLastModifiedTime()
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
        self.absolutePath = existingFile.getAbsolutePath()
        self.relativePath = existingFile.getRelativePath()
        self.lastModifiedTime = existingFile.getLastModifiedTime()
        self.lastAccessedTime = existingFile.getLastAccessedTime()
        self.creationTime = existingFile.getCreationTime()
        self.fileSize = existingFile.getFileSize()
        self.deletedTime = datetime.now().timestamp()

    def __getstate__(self):
        state = super().__getstate__()
        state['deletedTime'] = self.deletedTime
        return state

    def __setstate__(self, state):
        super().__setstate__(state)
        self.deletedTime = state['deletedTime']

    def __str__(self):
        return f"CustomFileInfo: {self.absolutePath}, {self.relativePath}, {self.fileSize}, {self.creationTime}, {self.lastModifiedTime}, {self.lastAccessedTime}, {self.deletedTime}"

    def getDeletedTime(self):
        return self.deletedTime

    def isFileNewestCopy(self, otherFile):
        # Override function so that if a file is deleted on one computer but then later modified on the other computer, the file will not be deleted
        return self.deletedTime > otherFile.getLastModifiedTime()
