# gui/MainContent/EpisodeDetailsPage.py

from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QScrollArea, QSizePolicy, QPushButton
from PySide6.QtCore import Qt
from gui.RatingWidgets.RatingWidget import RatingWidget

class EpisodeDetailsPage(QWidget):
    def __init__(self, navigation_controller, api_manager, rating_manager, show, episode):
        super().__init__()
        self.nav = navigation_controller
        self.api_manager = api_manager
        self.rating_manager = rating_manager
        self.show = show
        self.episode = episode

        layout = QVBoxLayout()
        self.setLayout(layout)

        # Episode details
        show_name = show.get('name', 'Unknown Name')
        ep_num = episode.get('episode_number', '?')
        name = episode.get('name', 'Unknown Episode')
        air_date = episode.get('air_date', 'Unknown Date')
        overview = episode.get('overview', 'No overview available.')
        global_rating = episode.get('vote_average', 'No rating available.')

        # Title
        show_label = QLabel(f"<h1>{show_name}</h1>")
        show_label.setTextFormat(Qt.RichText)
        layout.addWidget(show_label)

        episode_label = QLabel(f"Episode {ep_num}: {name}")
        episode_label.setWordWrap(True)
        layout.addWidget(episode_label)

        # Scrollable overview
        overview_label = QLabel(overview)
        overview_label.setWordWrap(True)
        overview_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)

        overview_scroll = QScrollArea()
        overview_scroll.setWidget(overview_label)
        overview_scroll.setWidgetResizable(True)
        overview_scroll.setFixedHeight(80)
        layout.addWidget(overview_scroll)

        # Air Date
        layout.addWidget(QLabel(f"Air Date: {air_date}"))

        # Global Rating
        layout.addWidget(QLabel(f"Global Rating: {global_rating}"))

        # Insert the reusable rating widget here
        content_id = f"tv:{show.get('id')}-S{episode.get('season_number')}-E{ep_num}"
        # Or whichever ID scheme you use for episodes
        rating_widget = RatingWidget(
            parent=self,
            rating_manager=rating_manager,
            content_id=content_id,
            title_text="Rate this Episode"
        )
        layout.addWidget(rating_widget)