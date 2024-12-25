# gui/MainContent/ResultsPage.py
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QScrollArea, QHBoxLayout, QPushButton
)
from PySide6.QtGui import QPixmap, QIcon
from PySide6.QtCore import Qt, QSize

from gui.MainContent.MovieDetailsPage import MovieDetailsPage
from gui.MainContent.ShowDetailsPage import ShowDetailsPage
import requests

class ResultsPage(QWidget):
    def __init__(self, navigation_controller, api_manager, rating_manager, results, is_movie):
        super().__init__()
        self.nav = navigation_controller
        self.api_manager = api_manager
        self.rating_manager = rating_manager
        self.results = results
        self.is_movie = is_movie

        main_layout = QVBoxLayout(self)
        main_layout.addWidget(QLabel("<h2>Search Results:</h2>"))

        # Create a scroll area to hold results
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_content = QWidget()
        self.results_layout = QVBoxLayout(scroll_content)

        # Reduce vertical spacing between results
        self.results_layout.setSpacing(4)

        for result in self.results:
            # Poster path
            poster_path = result.get('poster_path')  # e.g. "/4edFyasCrkH4MKs6H4mHqlrxA6b.jpg"
            btn = self.create_result_button(result, poster_path)
            self.results_layout.addWidget(btn)

        # Add stretch to push everything up
        self.results_layout.addStretch()

        scroll_content.setLayout(self.results_layout)
        scroll_area.setWidget(scroll_content)
        main_layout.addWidget(scroll_area)

    def create_result_button(self, result, poster_path):
        """
        Create a QPushButton with an icon (the poster) on the left
        and text also left-aligned. The text is the movie/show title + date.
        """
        if self.is_movie:
            title = result.get('title', 'Unknown Title')
            date = result.get('release_date', 'Unknown Date')
            button_text = f"{title} ({date})"
            clicked_fn = lambda _, r=result: self.show_movie_details(r)
        else:
            name = result.get('name', 'Unknown Name')
            date = result.get('first_air_date', 'Unknown Date')
            button_text = f"{name} ({date})"
            clicked_fn = lambda _, r=result: self.show_tv_details(r)

        btn = QPushButton(button_text)
        btn.clicked.connect(clicked_fn)

        # Left-align text
        btn.setStyleSheet("text-align: left;")

        # If there's a poster path, fetch image and set as icon
        if poster_path:
            pixmap_icon = self.fetch_and_scale_poster(poster_path)
            if pixmap_icon is not None:
                btn.setIcon(QIcon(pixmap_icon))
                # Icon size, e.g. 60x90 for a slightly bigger image
                btn.setIconSize(QSize(60, 90))

        return btn

    def fetch_and_scale_poster(self, poster_path):
        """
        Build a TMDB URL at a decent size (e.g. w154 or w342), 
        download it, and return a scaled QPixmap for the button.
        """
        # Let's pick "w154" for better quality than w92
        base_url = "https://image.tmdb.org/t/p/w154"
        url = f"{base_url}{poster_path}"
        try:
            response = requests.get(url)
            response.raise_for_status()
            pixmap = QPixmap()
            if pixmap.loadFromData(response.content):
                # Optionally do further scaling if needed
                return pixmap
        except Exception as e:
            print("Error fetching poster:", e)
        return None

    def show_movie_details(self, movie):
        movie_details_page = MovieDetailsPage(self.nav, self.api_manager, self.rating_manager, movie)
        self.nav.push(movie_details_page)

    def show_tv_details(self, tv_show):
        show_id = "tv:" + str(tv_show.get('id'))
        detailed_show = self.api_manager.get_content_details(show_id)
        show_details_page = ShowDetailsPage(self.nav, self.api_manager, self.rating_manager, detailed_show)
        self.nav.push(show_details_page)