# gui/DetailsPage.py
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QSizePolicy

class DetailsPage(QWidget):
    def __init__(self, navigation_controller, api_manager, content, is_movie):
        super().__init__()
        self.nav = navigation_controller
        self.api_manager = api_manager
        self.content = content
        self.is_movie = is_movie

        layout = QVBoxLayout()

        if is_movie:
            title = content.get('title', 'Unknown Title')
            date = content.get('release_date', 'Unknown Date')
            overview = content.get('overview', 'No overview available.')
            rating = content.get('vote_average', 'No rating available.')
            layout.addWidget(QLabel(f"Title: {title}"))
            layout.addWidget(QLabel(f"Release Date: {date}"))
        else:
            title = content.get('name', 'Unknown Name')
            date = content.get('first_air_date', 'Unknown Date')
            overview = content.get('overview', 'No overview available.')
            rating = content.get('vote_average', 'No rating available.')
            layout.addWidget(QLabel(f"Name: {title}"))
            layout.addWidget(QLabel(f"First Air Date: {date}"))

        overview_label = QLabel(f"Overview: {overview}")
        overview_label.setWordWrap(True)
        overview_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        layout.addWidget(overview_label)

        rating_label = QLabel(f"Rating: {rating}")
        rating_label.setWordWrap(True)
        rating_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        layout.addWidget(rating_label)

        rate_button = QPushButton("Rate this Content")
        rate_button.clicked.connect(self.open_rating_dialog)
        layout.addWidget(rate_button)

        layout.addWidget(rate_button)
        self.setLayout(layout)

    def open_rating_dialog(self):
        # Placeholder for rating dialog logic
        pass