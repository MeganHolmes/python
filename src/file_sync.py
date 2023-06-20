
# Import general packages
from __future__ import absolute_import
import sys

# Import Qt packages
from PyQt6.QtWidgets import (QApplication, QWidget, QLabel, QPushButton,
                             QCheckBox, QHBoxLayout, QVBoxLayout, QMainWindow, QFileDialog, QTextEdit)

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon

# Import project files
import comms.file
from file_sync.file_manager import FileManager, FileInfo

class FileSyncGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.primaryFileManager = FileManager()
        self.secondaryFileManager = FileManager()
        self.initializeUI()

    def initializeUI(self):
        self.mainContainer = QWidget()
        self.initBasicParameters()
        self.setUpCheckboxes()
        self.setUpButtons()
        self.setUpConsole()
        self.arrangeContainers()

        self.show() # Display the window on the screen

    def initBasicParameters(self):
        self.setWindowTitle("File Synchronization Manager")
        xlocation = 100
        ylocation = 100
        width = 1000
        height = 600
        self.setGeometry(xlocation, ylocation, width, height)
        self.setMinimumWidth(300)
        self.setMinimumHeight(100)
        self.setMaximumWidth(1920)
        self.setMaximumHeight(1080)
        self.setWindowIcon(QIcon('../assets/WWR_logo.png')) # TODO: Fix this

    def setUpButtons(self):
        self.primarySyncFolderButton = QPushButton("Set Primary Local Sync Folder", self)
        self.primarySyncFolderButton.clicked.connect(self.setSyncFolder)

        self.secondarySyncFolderButton = QPushButton("Set Secondary Local Sync Folder", self)
        self.secondarySyncFolderButton.clicked.connect(self.setSyncFolder)
        self.secondarySyncFolderButton.setEnabled(False)

        discoverFilesButton = QPushButton("Discover Files", self)
        discoverFilesButton.clicked.connect(self.discoverFilesTrigger)

        startSyncButton = QPushButton("Start Sync", self)
        startSyncButton.clicked.connect(self.startSyncTrigger)

        clearConsoleButton = QPushButton("Clear Console", self)
        clearConsoleButton.clicked.connect(self.clearConsoleTrigger)


        self.buttonContainer = QHBoxLayout()
        self.buttonContainer.addWidget(self.primarySyncFolderButton)
        self.buttonContainer.addWidget(self.secondarySyncFolderButton)
        self.buttonContainer.addWidget(discoverFilesButton)
        self.buttonContainer.addWidget(startSyncButton)
        self.buttonContainer.addWidget(clearConsoleButton)

    def setUpCheckboxes(self):
        self.localModeCheckbox = QCheckBox("Local Mode", self)
        self.localModeCheckbox.toggled.connect(self.localModeTrigger)

        self.verboseCheckbox = QCheckBox("Verbose", self)

        self.checkboxContainer = QHBoxLayout()
        self.checkboxContainer.addWidget(self.localModeCheckbox)
        self.checkboxContainer.addWidget(self.verboseCheckbox)

    def setUpConsole(self):
        self.console = QTextEdit(self)
        self.console.setReadOnly(True)
        # self.console.setAcceptRichText(False)
        # self.console.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy. ScrollBarAlwaysOn)

    def arrangeContainers(self):
        self.verticalContainer = QVBoxLayout()
        self.verticalContainer.addLayout(self.checkboxContainer)
        self.verticalContainer.addLayout(self.buttonContainer)
        self.verticalContainer.addWidget(self.console)
        self.mainContainer.setLayout(self.verticalContainer)
        self.setCentralWidget(self.mainContainer)

    def setSyncFolder(self):
        syncPath = QFileDialog.getExistingDirectory(self)
        if syncPath == "":
            self.console.append("No path selected")
        else:
            self.console.append("Path selected: " + syncPath)
            if app.sender() == self.primarySyncFolderButton:
                self.primaryFileManager.setRootPath(syncPath)
            elif app.sender() == self.secondarySyncFolderButton:
                self.secondaryFileManager.setRootPath(syncPath)
            else:
                self.console.append("ERROR: Unknown sender")


    def discoverFilesTrigger(self):
        if self.primaryFileManager.getRootPath() != "":
            self.console.append("Discovering files for " + self.primaryFileManager.getRootPath())
            self.primaryFileManager.discoverFiles()

            if self.verboseCheckbox.isChecked():
                self.console.append("Files Found:")
                self.addListToConsole(self.primaryFileManager.getAllFiles())

        if self.secondaryFileManager.getRootPath() != "" and self.localModeCheckbox.isChecked():
            self.secondaryFileManager.discoverFiles()
            self.console.append("Discovering files for " + self.secondaryFileManager.getRootPath())

            if self.verboseCheckbox.isChecked():
                self.console.append("Files Found:")
                self.addListToConsole(self.secondaryFileManager.getAllFiles())

    def localModeTrigger(self):
        if self.localModeCheckbox.isChecked():
            self.secondarySyncFolderButton.setEnabled(True)
        else:
            self.secondarySyncFolderButton.setEnabled(False)

    def clearConsoleTrigger(self):
        self.console.clear()

    def addListToConsole(self, list):
        if list is not None:
            for item in list:
                self.console.append("   " + item.getRelativePath())
        else:
            self.console.append("   Empty List")

    def startSyncTrigger(self):
        if self.localModeCheckbox.isChecked():
            self.performLocalSync()
        else:
            self.console.append("Remote sync isn't implemented yet")

    def performLocalSync(self):
        self.console.append("Starting local sync. Getting files from secondary manager")
        secondaryFiles = self.secondaryFileManager.getAllFiles()

        self.console.append("Comparing files with primary manager")
        filesNeededFromSecondary = self.primaryFileManager.compareFiles(secondaryFiles)

        if self.verboseCheckbox.isChecked():
            self.console.append("Files needing transfer from secondary manager:")
            self.addListToConsole(filesNeededFromSecondary)

        self.console.append("Transferring secondary files")
        for neededFile in filesNeededFromSecondary:
            destinationPath = comms.file.concatenatePaths(self.primaryFileManager.getRootPath(), neededFile.getRelativePath())
            comms.file.copyFile(neededFile.getAbsolutePath(), destinationPath)

            if self.verboseCheckbox.isChecked():
                self.console.append("   " + neededFile.getRelativePath() + " Copied")

        self.console.append("Getting files from primary manager")
        primaryFiles = self.primaryFileManager.getAllFiles()

        self.console.append("Comparing files with secondary manager")
        filesNeededFromPrimary = self.secondaryFileManager.compareFiles(primaryFiles)

        if self.verboseCheckbox.isChecked():
            self.console.append("Files needing transfer from primary manager:")
            self.addListToConsole(filesNeededFromPrimary)

        self.console.append("Transferring primary files")
        for neededFile in filesNeededFromPrimary:
            destinationPath = comms.file.concatenatePaths(self.secondaryFileManager.getRootPath(), neededFile.getRelativePath())
            comms.file.copyFile(neededFile.getAbsolutePath(), destinationPath)

            if self.verboseCheckbox.isChecked():
                self.console.append("   " + neededFile.getRelativePath() + " Copied")


# Run the program
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = FileSyncGUI()
    sys.exit(app.exec())
