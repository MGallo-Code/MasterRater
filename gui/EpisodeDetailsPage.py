# gui/EpisodeDetailsPage.py
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QScrollArea, QSizePolicy

class EpisodeDetailsPage(QWidget):
    def __init__(self, navigation_controller, api_manager, show, episode):
        super().__init__()
        self.nav = navigation_controller
        self.api_manager = api_manager
        self.show = show
        self.episode = episode

        # Main layout
        layout = QVBoxLayout()

        # Episode details
        ep_num = episode.get('episode_number', '?')
        name = episode.get('name', 'Unknown Episode')
        air_date = episode.get('air_date', 'Unknown Date')
        overview = episode.get('overview', 'No overview available.')
        rating = episode.get('vote_average', 'No rating available.')

        # Title (long titles get wrapped)
        episode_label = QLabel(f"Episode {ep_num}: {name}")
        episode_label.setWordWrap(True)  # Wraps long titles
        episode_label.setStyleSheet("font-size: 16px; font-weight: bold;")
        layout.addWidget(episode_label)

        # Scrollable area for long overviews
        overview_label = QLabel(f"Overview: {overview}")
        overview_label.setWordWrap(True)  # Wraps text
        overview_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)

        overview_scroll = QScrollArea()
        overview_scroll.setWidget(overview_label)
        overview_scroll.setWidgetResizable(True)
        overview_scroll.setFixedHeight(150)  # Limit visible height
        layout.addWidget(overview_scroll)

        # Air Date
        air_date_label = QLabel(f"Air Date: {air_date}")
        layout.addWidget(air_date_label)

        # Rating
        rating_label = QLabel(f"Rating: {rating}")
        layout.addWidget(rating_label)

        # Rate Button
        rate_button = QPushButton("Rate this Episode")
        rate_button.clicked.connect(self.open_rating_dialog)
        layout.addWidget(rate_button)

        # Set layout
        self.setLayout(layout)

    def open_rating_dialog(self):
        # Placeholder for rating dialog logic
        print("Opening rating dialog...")