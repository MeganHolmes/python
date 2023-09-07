# This module is the controller that controlls the high-level actions of the file-sync program.
# It sends and receives data from the GUI, manages the high-level states of the program, and
# sends commands to the fileManager class.

# General Imports
import time
import os

# Project Imports
import IO.file
from file_sync.fileManager import FileManager

class FileSyncController:
    def __init__(self, guiReference):
        self.gui = guiReference
        self.installLocation = os.path.expandvars("%USERPROFILE%\AppData\Local\Focus\File Sync") # TODO: Do this smarter
        self.primaryFileManager = FileManager(self.installLocation, "Primary")
        self.secondaryFileManager = FileManager(self.installLocation, "Secondary")
        self.localMode = False
        self.state = "initial"
        self.lastRunTimestamp = time.perf_counter() # When this program isn't using a manual trigger, we will use this to dermine when to transition from idle to running again



    def runLocal(self): # TODO: Make the state transitons better logic
        if self.state == "initial":
            self.discoverFilesTrigger()
            self.state = "checkLocalDeletedFiles"

        elif self.state == "checkLocalDeletedFiles":
            self.primaryFileManager.compareAgainstLocalSave()
            self.primaryFileManager.saveData()
            self.secondaryFileManager.compareAgainstLocalSave()
            self.secondaryFileManager.saveData()
            self.state = "sendPrimaryDeletedFiles"

        elif self.state == "sendPrimaryDeletedFiles":
            deletedFiles = self.primaryFileManager.getDeletedFiles()
            self.gui.verboseAppendToConsole("Primary Deleted File List:")
            self.gui.addListToConsole(deletedFiles)
            _, removeFromDeleted = self.secondaryFileManager.clearDeletedFiles(deletedFiles)
            self.primaryFileManager.removeDeletedFiles(removeFromDeleted)
            self.state = "sendSecondaryDeletedFiles"

        elif self.state == "sendSecondaryDeletedFiles":
            deletedFiles = self.secondaryFileManager.getDeletedFiles()
            self.gui.verboseAppendToConsole("Secondary Deleted File List:")
            self.gui.addListToConsole(deletedFiles)
            updateRequired, removeFromDeleted = self.primaryFileManager.clearDeletedFiles(deletedFiles)
            self.secondaryFileManager.removeDeletedFiles(removeFromDeleted)
            if updateRequired:
                self.gui.appendToConsole("Files were deleted. Updating managers")
                self.discoverFilesTrigger() # If any files were deleted we need to rediscover the files
                self.primaryFileManager.saveData()
                self.secondaryFileManager.saveData()
            self.state = "transferPrimaryFiles"

        elif self.state == "transferPrimaryFiles":
            self.processPrimaryLocal()
            self.secondaryFileManager.saveData()
            self.state = "transferSecondaryFiles"

        elif self.state == "transferSecondaryFiles":
            self.processSecondaryLocal()
            self.primaryFileManager.saveData()
            self.state = "idle"

        elif self.state == "idle":
            self.gui.appendToConsole("System in idle mode")

        self.lastRunTimestamp = time.perf_counter()


    def updateLocalMode(self, newMode):
        self.localMode = newMode

    def reset(self):
        self.state = "initial"
        self.primaryFileManager.reset()
        self.secondaryFileManager.reset()

    def deleteSavedData(self):
        self.primaryFileManager.deleteSavedData()
        self.secondaryFileManager.deleteSavedData()

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

    def processPrimaryLocal(self):
        self.gui.appendToConsole("Getting files from primary manager")
        primaryFiles = self.primaryFileManager.getAllFiles()

        self.gui.appendToConsole("Comparing files with secondary manager")
        filesNeededFromPrimary = self.secondaryFileManager.compareFiles(primaryFiles)

        self.gui.verboseAppendToConsole("Files needing transfer from primary manager:")
        self.gui.addListToConsole(filesNeededFromPrimary)

        self.gui.appendToConsole("Transferring primary files")
        for neededFile in filesNeededFromPrimary:
            destinationPath = IO.file.concatenatePaths(self.secondaryFileManager.getRootPath(), neededFile.getRelativePath())
            IO.file.copyFile(neededFile.getAbsolutePath(), destinationPath)

            self.gui.verboseAppendToConsole("   " + neededFile.getRelativePath() + " Copied")

    def processSecondaryLocal(self):
        self.gui.appendToConsole("Getting files from secondary manager")
        secondaryFiles = self.secondaryFileManager.getAllFiles()

        self.gui.appendToConsole("Comparing files with primary manager")
        filesNeededFromSecondary = self.primaryFileManager.compareFiles(secondaryFiles)

        self.gui.verboseAppendToConsole("Files needing transfer from secondary manager:")
        self.gui.addListToConsole(filesNeededFromSecondary)

        self.gui.appendToConsole("Transferring secondary files")
        for neededFile in filesNeededFromSecondary:
            destinationPath = IO.file.concatenatePaths(self.primaryFileManager.getRootPath(), neededFile.getRelativePath())
            IO.file.copyFile(neededFile.getAbsolutePath(), destinationPath)

            self.gui.verboseAppendToConsole("   " + neededFile.getRelativePath() + " Copied")
