import sys
from gui.MainWindow import MainWindow
from PyQt6.QtWidgets import QApplication

class App:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.window = MainWindow()

    def run(self):
        self.window.show()
        sys.exit(self.app.exec())