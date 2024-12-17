# gui/App.py

import sys
from gui.MainWindow import MainWindow
from PySide6.QtWidgets import QApplication

class App:
    def __init__(self):
        self.app = QApplication([])
        self.window = MainWindow()

    def run(self):
        self.window.show()
        sys.exit(self.app.exec())