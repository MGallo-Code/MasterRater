# gui/ResultsPage.py
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QScrollArea

class ResultsPage(QWidget):
    def __init__(self, navigation_controller, api_manager, results, is_movie):
        super().__init__()
        self.nav = navigation_controller
        self.api_manager = api_manager
        self.results = results
        self.is_movie = is_movie

        main_layout = QVBoxLayout()
        main_layout.addWidget(QLabel("<h2>Search Results:</h2>"))

        # Create a scroll area for the results
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_content = QWidget()
        results_layout = QVBoxLayout()

        for result in self.results:
            if self.is_movie:
                title = result.get('title', 'Unknown Title')
                date = result.get('release_date', 'Unknown Date')
                btn = QPushButton(f"{title} ({date})")
                btn.clicked.connect(lambda _, r=result: self.show_movie_details(r))
            else:
                name = result.get('name', 'Unknown Name')
                date = result.get('first_air_date', 'Unknown Date')
                btn = QPushButton(f"{name} ({date})")
                btn.clicked.connect(lambda _, r=result: self.show_tv_details(r))
            results_layout.addWidget(btn)

        results_layout.addStretch()
        scroll_content.setLayout(results_layout)
        scroll_area.setWidget(scroll_content)
        main_layout.addWidget(scroll_area)

        self.setLayout(main_layout)

    def show_movie_details(self, movie):
        from gui.MovieDetailsPage import MovieDetailsPage
        movie_details_page = MovieDetailsPage(self.nav, self.api_manager, movie)
        self.nav.push(movie_details_page)

    def show_tv_details(self, tv_show):
        from gui.ShowDetailsPage import ShowDetailsPage
        show_id = tv_show.get('id')
        detailed_show = self.api_manager.get_details(show_id, 'tv')
        show_details_page = ShowDetailsPage(self.nav, self.api_manager, detailed_show)
        self.nav.push(show_details_page)