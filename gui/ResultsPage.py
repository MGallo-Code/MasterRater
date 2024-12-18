# gui/ResultsPage.py
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from gui.MovieDetailsPage import MovieDetailsPage
from gui.ShowDetailsPage import ShowDetailsPage

class ResultsPage(QWidget):
    def __init__(self, navigation_controller, api_manager, results, is_movie):
        super().__init__()
        self.nav = navigation_controller
        self.api_manager = api_manager
        self.results = results
        self.is_movie = is_movie

        layout = QVBoxLayout()
        layout.addWidget(QLabel("Search Results:"))
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
            layout.addWidget(btn)

        self.setLayout(layout)

    def show_movie_details(self, movie):
        movie_details_page = MovieDetailsPage(self.nav, self.api_manager, movie, True)
        self.nav.push(movie_details_page)

    def show_tv_details(self, tv_show):
        # Get full show details before displaying the show details page
        show_id = tv_show.get('id')
        detailed_show = self.api_manager.get_details(show_id, 'tv')
        show_details_page = ShowDetailsPage(self.nav, self.api_manager, detailed_show)
        self.nav.push(show_details_page)