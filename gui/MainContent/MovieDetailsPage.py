# gui/MovieDetailsPage.py
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QSizePolicy

class MovieDetailsPage(QWidget):
    def __init__(self, navigation_controller, api_manager, movie):
        super().__init__()
        self.nav = navigation_controller
        self.api_manager = api_manager
        self.movie = movie

        layout = QVBoxLayout()

        title = movie.get('title', 'Unknown Title')
        date = movie.get('release_date', 'Unknown Date')
        overview = movie.get('overview', 'No overview available.')
        rating = movie.get('vote_average', 'No rating available.')

        title_label = QLabel(f"<h2>{title}</h2>")
        layout.addWidget(title_label)

        date_label = QLabel(f"Release Date: {date}")
        layout.addWidget(date_label)

        overview_label = QLabel(f"Overview: {overview}")
        overview_label.setWordWrap(True)
        overview_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        layout.addWidget(overview_label)

        rating_label = QLabel(f"Rating: {rating}")
        rating_label.setWordWrap(True)
        rating_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        layout.addWidget(rating_label)

        rate_button = QPushButton("Rate this Movie")
        rate_button.clicked.connect(self.open_rating_dialog)
        layout.addWidget(rate_button)

        self.setLayout(layout)

    def open_rating_dialog(self):
        print("Opening rating dialog...")