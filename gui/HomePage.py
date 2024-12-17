# gui/HomePage.py

from PySide6.QtWidgets import QMainWindow, QStackedWidget, QHBoxLayout, QVBoxLayout, QWidget, QPushButton
from PySide6.QtCore import Qt

class HomePage(QWidget):
    def __init__(self, main_window):
        super().__init__()
        layout = QVBoxLayout()
        self.main_window = main_window
        
        view_ratings_button = QPushButton("View Your Ratings")
        view_ratings_button.clicked.connect(lambda: self.main_window.stacked_widget.setCurrentWidget(ViewRatingsPage(self.main_window)))
        
        rate_new_button = QPushButton("Rate New Content")
        rate_new_button.clicked.connect(lambda: self.main_window.stacked_widget.setCurrentWidget(self.main_window.search_page))

        layout.addWidget(view_ratings_button)
        layout.addWidget(rate_new_button)
        self.setLayout(layout)