from PyQt6.QtWidgets import QMainWindow, QStackedWidget, QHBoxLayout, QVBoxLayout, QWidget, QPushButton, QComboBox, QLineEdit, QLabel
from PyQt6.QtCore import Qt

class SearchPage(QWidget):
    def __init__(self, main_window):
        super().__init__()
        layout = QVBoxLayout()
        self.main_window = main_window

        self.prompt_label = QLabel("Would you like to search for a movie or a TV show?")
        self.type_selector = QComboBox()
        self.type_selector.addItems(["Movie", "TV Show"])

        self.search_input = QLineEdit()
        self.search_button = QPushButton("Search")
        self.search_button.clicked.connect(self.perform_search)

        layout.addWidget(self.prompt_label)
        layout.addWidget(self.type_selector)
        layout.addWidget(self.search_input)
        layout.addWidget(self.search_button)
        self.setLayout(layout)

    def perform_search(self):
        # Perform the API search here
        content_type = self.type_selector.currentText().lower()
        query = self.search_input.text()
        results = self.main_window.api_manager.get_search(query, content_type)

        # Pass results to next page and display
        if content_type == 'movie':
            self.main_window.movie_page.display_results(results)
            self.main_window.stacked_widget.setCurrentWidget(self.main_window.movie_page)
        else:
            self.main_window.tv_show_page.display_results(results)
            self.main_window.stacked_widget.setCurrentWidget(self.main_window.tv_show_page)