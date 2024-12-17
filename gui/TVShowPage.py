# gui/TVShowPage.py

from PySide6.QtWidgets import QMainWindow, QStackedWidget, QHBoxLayout, QVBoxLayout, QWidget, QPushButton, QComboBox, QLineEdit, QLabel
from PySide6.QtCore import Qt

class TVShowPage(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.layout = QVBoxLayout()
        self.results_label = QLabel("Results will appear here.")
        self.layout.addWidget(self.results_label)
        self.setLayout(self.layout)

    def display_results(self, results):
        # Clear the layout first (if displaying multiple times)
        self.clear_layout(self.layout)

        self.layout.addWidget(QLabel("Search Results:"))
        for i, show in enumerate(results):
            # For TV shows, the API returns 'name' and 'first_air_date'
            show_name = show.get('name', 'Unknown Name')
            show_date = show.get('first_air_date', 'Unknown Date')
            result_button = QPushButton(f"{show_name} ({show_date})")
            # Connect button to a method to display details for this particular show
            # Use 'show' directly in the lambda to avoid late-binding issues
            result_button.clicked.connect(lambda _, s=show: self.display_tv_details(s))
            self.layout.addWidget(result_button)

    def display_tv_details(self, show):
        # Clear existing layout items
        self.clear_layout(self.layout)

        show_name = show.get('name', 'Unknown Name')
        show_date = show.get('first_air_date', 'Unknown Date')
        show_overview = show.get('overview', 'No overview available.')
        show_rating = show.get('vote_average', 'No rating available.')

        self.layout.addWidget(QLabel(f"Name: {show_name}"))
        self.layout.addWidget(QLabel(f"First Air Date: {show_date}"))
        self.layout.addWidget(QLabel(f"Overview: {show_overview}"))
        self.layout.addWidget(QLabel(f"Rating: {show_rating}"))

        rate_button = QPushButton("Rate this TV Show")
        rate_button.clicked.connect(lambda: self.open_rating_dialog(show))
        self.layout.addWidget(rate_button)

    def open_rating_dialog(self, show):
        # Code for opening rating dialog and saving rating would go here.
        pass

    def clear_layout(self, layout):
        # Utility method to clear layout widgets
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()