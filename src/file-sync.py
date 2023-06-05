
# Import general packages
import sys

# Import Qt packages
from PyQt6.QtWidgets import (QApplication, QWidget, QLabel, QPushButton,
                             QCheckBox, QHBoxLayout, QVBoxLayout, QMainWindow, QFileDialog, QTextEdit)

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon

# Import project files

class ManagerWindow(QMainWindow):
    def __init__(self):
        super().__init__()
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
        syncFolderButton = QPushButton("Set Sync Folder", self)
        syncFolderButton.clicked.connect(self.setSyncFolder)

        button1 = QPushButton("Option 1", self)
        button1.clicked.connect(self.buttonClicked)
        button2 = QPushButton("Option 2", self)
        button2.clicked.connect(self.buttonClicked)
        button2.setEnabled(False)

        self.buttonContainer = QHBoxLayout()
        self.buttonContainer.addWidget(syncFolderButton)
        self.buttonContainer.addWidget(button1)
        self.buttonContainer.addWidget(button2)

    def setUpCheckboxes(self):
        checkbox1 = QCheckBox("Test box 1", self)
        checkbox1.toggled.connect(self.checkboxTrigger)
        checkbox2 = QCheckBox("Test box 2", self)
        checkbox2.toggled.connect(self.checkboxTrigger)

        self.checkboxContainer = QHBoxLayout()
        self.checkboxContainer.addWidget(checkbox1)
        self.checkboxContainer.addWidget(checkbox2)

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

    def buttonClicked(self):
        # Placeholder
        self.console.append("Button Clicked")

    def checkboxTrigger(self):
        # Placeholder
        self.console.append("Checkbox Triggered")

    def setSyncFolder(self):
        self.sync_path = QFileDialog.getExistingDirectory(self)
        self.console.append(self.sync_path)


# Run the program
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ManagerWindow()
    sys.exit(app.exec())
