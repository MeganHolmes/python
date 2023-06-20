
# Import general packages
from __future__ import absolute_import
import sys
from PyQt6.QtWidgets import QApplication

# Import project files
from file_sync.fileSyncGUI import FileSyncGUI

# Run the program
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = FileSyncGUI(app)
    sys.exit(app.exec())
