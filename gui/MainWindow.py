# gui/MainWindow.py
from PySide6.QtWidgets import QMainWindow, QComboBox, QLineEdit, QHBoxLayout, QVBoxLayout, QWidget, QPushButton
from PySide6.QtCore import Qt
from gui.NavigationController import NavigationController
from gui.HomePage import HomePage
from gui.ResultsPage import ResultsPage
from utils.APIManager import APIManager

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Master Rater")
        self.resize(800, 600)

        # Initialize Rating API Manager and Navigation Controller
        self.api_manager = APIManager()
        self.nav_controller = NavigationController()

        # Set up main layout
        main_layout = QVBoxLayout()

        # Create the navigation bar
        nav_widget = self.create_navigation_bar()
        main_layout.addWidget(nav_widget)

        # Create the content area
        self.content_area = QWidget()
        self.content_layout = QVBoxLayout()
        self.content_layout.setContentsMargins(0, 0, 0, 0)
        self.content_area.setLayout(self.content_layout)

        # Add the content area to the main layout
        main_layout.addWidget(self.content_area)

        # Set the central widget
        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        # Connect navigation signals
        self.nav_controller.current_widget_changed.connect(self.set_current_widget)

        # Initially show home page
        self.base_page = HomePage()
        self.nav_controller.reset(self.base_page)

    def create_navigation_bar(self):
        nav_bar = QHBoxLayout()

        # Back Button
        self.back_button = QPushButton("<- Back")
        self.back_button.clicked.connect(self.go_back)
        nav_bar.addWidget(self.back_button)

        # Forward Button
        self.forward_button = QPushButton("Forward ->")
        self.forward_button.clicked.connect(self.go_forward)
        nav_bar.addWidget(self.forward_button)

        # Content Type Selector
        self.type_selector = QComboBox()
        self.type_selector.addItems(["Movie", "TV Show"])
        nav_bar.addWidget(self.type_selector)

        # Search Field
        self.search_field = QLineEdit()
        self.search_field.setPlaceholderText("Search...")
        nav_bar.addWidget(self.search_field)

        # Search Button
        search_button = QPushButton("Search")
        search_button.clicked.connect(self.perform_search)
        nav_bar.addWidget(search_button)

        # Ratings Button
        ratings_button = QPushButton("View Ratings")
        # Hook up as needed
        nav_bar.addWidget(ratings_button)

        # Wrap QHBoxLayout in a QWidget
        nav_widget = QWidget()
        nav_widget.setLayout(nav_bar)
        return nav_widget

    def go_back(self):
        if self.nav_controller.can_go_back():
            self.nav_controller.pop()
            self.update_navigation_buttons()

    def go_forward(self):
        if self.nav_controller.can_go_forward():
            self.nav_controller.forward()
            self.update_navigation_buttons()

    def perform_search(self):
        query = self.search_field.text().strip()
        if not query:
            return
        is_movie = (self.type_selector.currentText().lower() == "movie")
        content_type = 'movie' if is_movie else 'tv'
        results = self.api_manager.get_search(query, content_type)
        results_page = ResultsPage(self.nav_controller, self.api_manager, results, is_movie)
        self.nav_controller.push(results_page)
        self.update_navigation_buttons()

    def set_current_widget(self, widget):
        # Clear the content layout and add the current widget
        for i in reversed(range(self.content_layout.count())):
            item = self.content_layout.takeAt(i)
            w = item.widget()
            if w:
                w.setParent(None)
        self.content_layout.addWidget(widget)

        # Update navigation buttons
        self.update_navigation_buttons()

    def update_navigation_buttons(self):
        """Enable or disable Back/Forward buttons based on navigation state."""
        self.back_button.setEnabled(self.nav_controller.can_go_back())
        self.forward_button.setEnabled(self.nav_controller.can_go_forward())