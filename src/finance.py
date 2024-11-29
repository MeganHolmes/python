# System Imports
from __future__ import absolute_import
import sys
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QGridLayout, QVBoxLayout

# Project imports
import display.guiHelper

class financeGUI(QWidget):
    def __init__(self):
        """Constructor"""
        super().__init__()
        self.initializeUI()
        self.num_labels = 11

    def initializeUI(self):
        """Setup the inital state of the application"""
        self.setWindowTitle("Megan Finance")
        self.setUpMainWindow()
        self.show()

    def setUpMainWindow(self):
        self.category_names = ["Forecast", "Income", "Housing", "Home Purchase", "Car", "Food", "Rivian Stock", "Average Expenses", "Liabilities", "Taxes"]
        self.boxes = []

        for category in self.category_names:
            self.boxes.append(QVBoxLayout())

        self.labels = []

        for category_idx, name in enumerate(self.category_names):
            self.labels.append(QLabel(name))
            self.boxes[category_idx].addWidget(self.labels[category_idx])

        self.main_grid = QGridLayout()
        display.guiHelper.populateGrid(self.main_grid, self.boxes)
        self.setLayout(self.main_grid)




def main():
    app = QApplication([])
    window = financeGUI()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()