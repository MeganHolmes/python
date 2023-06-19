
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
from app.rsync import Rsync

class FileSyncGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.primaryRsyncManager = Rsync()
        self.secondaryRsyncManager = Rsync()
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

        loadFilesButton = QPushButton("Load Files", self)
        loadFilesButton.clicked.connect(self.loadFilesTrigger)

        prepareFilesButton = QPushButton("Prepare Files", self)
        prepareFilesButton.clicked.connect(self.prepareFilesTrigger)

        clearConsoleButton = QPushButton("Clear Console", self)
        clearConsoleButton.clicked.connect(self.clearConsoleTrigger)


        self.buttonContainer = QHBoxLayout()
        self.buttonContainer.addWidget(self.primarySyncFolderButton)
        self.buttonContainer.addWidget(self.secondarySyncFolderButton)
        self.buttonContainer.addWidget(discoverFilesButton)
        self.buttonContainer.addWidget(loadFilesButton)
        self.buttonContainer.addWidget(prepareFilesButton)
        self.buttonContainer.addWidget(clearConsoleButton)

    def setUpCheckboxes(self):
        self.localModeCheckbox = QCheckBox("Local Mode", self)
        self.localModeCheckbox.toggled.connect(self.localModeTrigger)

        self.checkboxContainer = QHBoxLayout()
        self.checkboxContainer.addWidget(self.localModeCheckbox)

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
                self.primaryRsyncManager.setRootPath(syncPath)
            elif app.sender() == self.primarySyncFolderButton:
                self.secondaryRsyncManager.setRootPath(syncPath)
            else:
                self.console.append("ERROR: Unknown sender")


    def discoverFilesTrigger(self):
        if self.primaryRsyncManager.getRootPath() != "":
            self.console.append("Discovering files for " + self.primaryRsyncManager.getRootPath())
            self.primaryRsyncManager.discoverFiles()
        if self.secondaryRsyncManager.getRootPath() != "" and self.localModeCheckbox.isChecked():
            self.secondaryRsyncManager.discoverFiles()
            self.console.append("Discovering files for " + self.secondaryRsyncManager.getRootPath())

    def localModeTrigger(self):
        if self.localModeCheckbox.isChecked():
            self.console.append("Local mode enabled")
            self.secondarySyncFolderButton.setEnabled(True)
        else:
            self.console.append("Local mode disabled")
            self.secondarySyncFolderButton.setEnabled(False)

    def clearConsoleTrigger(self):
        self.console.clear()

    def prepareFilesTrigger(self):
        if self.primaryRsyncManager.areFilesPresent():
            self.console.append("Preparing Primary files")
            self.primaryRsyncManager.prepareAllFiles()

        if self.secondaryRsyncManager.areFilesPresent():
            self.console.append("Preparing Secondary files")
            self.secondaryRsyncManager.prepareAllFiles()

    def loadFilesTrigger(self):
        if self.primaryRsyncManager.areFilesPresent():
            self.console.append("Loading Primary files")
            self.primaryRsyncManager.loadFilesIntoMemory()

        if self.secondaryRsyncManager.areFilesPresent():
            self.console.append("Loading Secondary files")
            self.secondaryRsyncManager.loadFilesIntoMemory()



# Run the program
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = FileSyncGUI()
    sys.exit(app.exec())
