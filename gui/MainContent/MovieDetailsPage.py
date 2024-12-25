# gui/MainContent/MovieDetailsPage.py

from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QSizePolicy, QScrollArea
from PySide6.QtCore import Qt
from gui.CustomWidgets.RatingWidget import RatingWidget

class MovieDetailsPage(QWidget):
    def __init__(self, navigation_controller, api_manager, rating_manager, movie):
        super().__init__()
        self.nav = navigation_controller
        self.api_manager = api_manager
        self.rating_manager = rating_manager
        self.movie = movie

        layout = QVBoxLayout()
        self.setLayout(layout)

        # Basic movie info
        title = movie.get('title', 'Unknown Title')
        date = movie.get('release_date', 'Unknown Date')
        overview = movie.get('overview', 'No overview available.')
        global_rating = movie.get('vote_average', 'No rating available.')

        title_label = QLabel(f"<h2>{title}</h2>")
        title_label.setTextFormat(Qt.RichText)
        layout.addWidget(title_label)

        layout.addWidget(QLabel(f"Release Date: {date}"))

        # Overview
        overview_label = QLabel(f"{overview}")
        overview_label.setWordWrap(True)
        overview_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        layout.addWidget(overview_label)

        layout.addWidget(QLabel(f"TMDB Global Rating: {global_rating}"))

        # Insert reusable rating widget
        content_id = f"movie:{movie.get('id')}"
        rating_widget = RatingWidget(
            parent=self,
            rating_manager=rating_manager,
            content_id=content_id,
            title_text="Rate this Movie"
        )
        layout.addWidget(rating_widget)