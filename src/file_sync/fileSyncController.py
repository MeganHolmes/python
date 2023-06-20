# This module is the controller that controlls the high-level actions of the file-sync program.
# It sends and receives data from the GUI, manages the high-level states of the program, and
# sends commands to the fileManager class.

# General Imports

# Project Imports
import comms.file
from file_sync.fileManager import FileManager

class FileSyncController:
    def __init__(self, guiReference):
        self.gui = guiReference
        self.primaryFileManager = FileManager()
        self.secondaryFileManager = FileManager()
        self.localMode = False

    def updateLocalMode(self, newMode):
        self.localMode = newMode

    def setRootPath(self, path, updatePrimary):
        if updatePrimary:
            self.primaryFileManager.setRootPath(path)
        else:
            self.secondaryFileManager.setRootPath(path)

    def discoverFilesTrigger(self):
        if self.primaryFileManager.getRootPath() != "":
            self.gui.appendToConsole("Discovering files for " + self.primaryFileManager.getRootPath())
            self.primaryFileManager.discoverFiles()

            self.gui.verboseAppendToConsole("Files Found:")
            self.gui.addListToConsole(self.primaryFileManager.getAllFiles())

        if self.secondaryFileManager.getRootPath() != "" and self.localMode:
            self.secondaryFileManager.discoverFiles()
            self.gui.appendToConsole("Discovering files for " + self.secondaryFileManager.getRootPath())

            self.gui.verboseAppendToConsole("Files Found:")
            self.gui.addListToConsole(self.secondaryFileManager.getAllFiles())

    def performLocalSync(self):
        self.gui.appendToConsole("Starting local sync. Getting files from secondary manager")
        secondaryFiles = self.secondaryFileManager.getAllFiles()

        self.gui.appendToConsole("Comparing files with primary manager")
        filesNeededFromSecondary = self.primaryFileManager.compareFiles(secondaryFiles)

        self.gui.verboseAppendToConsole("Files needing transfer from secondary manager:")
        self.gui.addListToConsole(filesNeededFromSecondary)

        self.gui.appendToConsole("Transferring secondary files")
        for neededFile in filesNeededFromSecondary:
            destinationPath = comms.file.concatenatePaths(self.primaryFileManager.getRootPath(), neededFile.getRelativePath())
            comms.file.copyFile(neededFile.getAbsolutePath(), destinationPath)

            self.gui.verboseAppendToConsole("   " + neededFile.getRelativePath() + " Copied")

        self.gui.appendToConsole("Getting files from primary manager")
        primaryFiles = self.primaryFileManager.getAllFiles()

        self.gui.appendToConsole("Comparing files with secondary manager")
        filesNeededFromPrimary = self.secondaryFileManager.compareFiles(primaryFiles)

        self.gui.verboseAppendToConsole("Files needing transfer from primary manager:")
        self.gui.addListToConsole(filesNeededFromPrimary)

        self.gui.appendToConsole("Transferring primary files")
        for neededFile in filesNeededFromPrimary:
            destinationPath = comms.file.concatenatePaths(self.secondaryFileManager.getRootPath(), neededFile.getRelativePath())
            comms.file.copyFile(neededFile.getAbsolutePath(), destinationPath)

            self.gui.verboseAppendToConsole("   " + neededFile.getRelativePath() + " Copied")

        self.gui.appendToConsole("Local sync finished")
