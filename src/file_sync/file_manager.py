
# Import general packages
from __future__ import absolute_import

# Import project files
import comms.file

class FileManager():
    def __init__(self):
        self.rootPath = ""
        self.allFiles = []

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
            if self.fileSize == otherFile.getFileSize():
                return True
            else:
                return self.fileSize > otherFile.getFileSize()
        else:
            return self.lastModifiedTime > otherFile.getLastModifiedTime()
