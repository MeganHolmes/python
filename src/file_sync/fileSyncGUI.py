# This file manages the GUI elements of the file sync program

# Import general packages
from __future__ import absolute_import

# Import Qt packages
from PyQt6.QtWidgets import (QWidget, QPushButton,
                             QCheckBox, QHBoxLayout, QVBoxLayout, QMainWindow, QFileDialog, QTextEdit)

from PyQt6.QtGui import QIcon

# Import project files
from file_sync.fileSyncController import FileSyncController

class FileSyncGUI(QMainWindow):
    def __init__(self, appReference):
        super().__init__()
        self.app = appReference
        self.controller = FileSyncController(self)
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
        discoverFilesButton.clicked.connect(self.controller.discoverFilesTrigger)

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
            if self.app.sender() == self.primarySyncFolderButton:
                self.controller.setRootPath(syncPath, True)
            elif self.app.sender() == self.secondarySyncFolderButton:
                self.controller.setRootPath(syncPath, False)
            else:
                self.console.append("ERROR: Unknown sender")


    def localModeTrigger(self):
        self.controller.updateLocalMode(self.localModeCheckbox.isChecked())
        if self.localModeCheckbox.isChecked():
            self.secondarySyncFolderButton.setEnabled(True)
        else:
            self.secondarySyncFolderButton.setEnabled(False)

    def clearConsoleTrigger(self):
        self.console.clear()

    def addListToConsole(self, list):
        if self.verboseCheckbox.isChecked():
            if list is not None:
                for item in list:
                    self.console.append("   " + item.getRelativePath())
            else:
                self.console.append("   Empty List")

    def startSyncTrigger(self):
        if self.localModeCheckbox.isChecked():
            self.controller.performLocalSync()
        else:
            self.console.append("Remote sync isn't implemented yet")

    def appendToConsole(self, data):
        self.console.append(data)

    def verboseAppendToConsole(self, data):
        if self.verboseCheckbox.isChecked():
            self.console.append(data)
