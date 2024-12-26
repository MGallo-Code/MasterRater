# gui/MainContent/MovieDetailsPage.py

from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QScrollArea
from PySide6.QtCore import Qt
from gui.CustomWidgets.RatingWidget import RatingWidget
from gui.CustomWidgets.MediaHeaderWidget import MediaHeaderWidget

class MovieDetailsPage(QWidget):
    def __init__(self, navigation_controller, api_manager, rating_manager, movie):
        super().__init__()
        self.nav = navigation_controller
        self.api_manager = api_manager
        self.rating_manager = rating_manager
        self.movie = movie

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0,0,0,0)

        # Insert the custom media header up top
        title = movie.get('title', 'Unknown Title')
        backdrop = movie.get('backdrop_path')
        poster = movie.get('poster_path')

        header_widget = MediaHeaderWidget(
            parent=self,
            title=title,
            backdrop_path=backdrop,
            poster_path=poster,
        )
        main_layout.addWidget(header_widget)

        # Then you can add rating, overview, etc. beneath the header
        rating_label = QLabel(f"TMDB Rating: {movie.get('vote_average', 'N/A')}")
        main_layout.addWidget(rating_label)

        overview = movie.get('overview', 'No overview provided.')
        overview_label = QLabel(overview)
        overview_label.setWordWrap(True)
        main_layout.addWidget(overview_label)

        # If you want a rating widget, etc. add them here
        content_id = f"movie:{movie.get('id')}"
        rating_widget = RatingWidget(
            parent=self,
            rating_manager=rating_manager,
            content_id=content_id,
            title_text="Rate this Movie"
        )
        main_layout.addWidget(rating_widget)

        main_layout.addStretch()