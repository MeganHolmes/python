
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

class ManagerWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.primarySyncPath = ""
        self.secondarySyncPath = ""
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
        primarySyncFolderButton = QPushButton("Set Primary Local Sync Folder", self)
        primarySyncFolderButton.clicked.connect(self.setPrimarySyncFolder)

        collectFilesButton = QPushButton("Collect Files", self)
        collectFilesButton.clicked.connect(self.collectFilesTrigger)

        self.secondarySyncFolderButton = QPushButton("Set Secondary Local Sync Folder", self)
        self.secondarySyncFolderButton.clicked.connect(self.setSecondarySyncFolder)
        self.secondarySyncFolderButton.setEnabled(False)

        clearConsoleButton = QPushButton("Clear Console", self)
        clearConsoleButton.clicked.connect(self.clearConsoleTrigger)


        self.buttonContainer = QHBoxLayout()
        self.buttonContainer.addWidget(primarySyncFolderButton)
        self.buttonContainer.addWidget(collectFilesButton)
        self.buttonContainer.addWidget(self.secondarySyncFolderButton)
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

    def setPrimarySyncFolder(self):
        self.primarySyncPath = QFileDialog.getExistingDirectory(self)
        if self.primarySyncPath == "":
            self.console.append("No path selected")
        else:
            self.console.append("Path selected: " + self.primarySyncPath)

    def setSecondarySyncFolder(self):
        self.secondarySyncPath = QFileDialog.getExistingDirectory(self)
        if self.secondarySyncPath == "":
            self.console.append("No path selected")
        else:
            self.console.append("Path selected: " + self.secondarySyncPath)

    def collectFilesTrigger(self):
        if self.primarySyncPath != "":
            self.allPrimaryFiles = comms.file.getFilesInDirectory(self.primarySyncPath)
            self.console.append("----- Inside " + self.primarySyncPath + " -----")
            self.displayList(self.allPrimaryFiles)
        if self.secondarySyncPath != "" and self.localModeCheckbox.isChecked():
            self.allSecondaryFiles = comms.file.getFilesInDirectory(self.secondarySyncPath)
            self.console.append("----- Inside " + self.secondarySyncPath + " -----")
            self.displayList(self.allSecondaryFiles)

    def displayList(self, list):
        if list is not []:
            for item in list:
                self.console.append(item)
        else:
            self.console.append("No items found")

    def localModeTrigger(self):
        if self.localModeCheckbox.isChecked():
            self.console.append("Local mode enabled")
            self.secondarySyncFolderButton.setEnabled(True)
        else:
            self.console.append("Local mode disabled")
            self.secondarySyncFolderButton.setEnabled(False)

    def clearConsoleTrigger(self):
        self.console.clear()



# Run the program
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ManagerWindow()
    sys.exit(app.exec())
