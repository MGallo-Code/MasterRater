# gui/MainContent/SeasonDetailsPage.py

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QScrollArea, QSizePolicy, QFrame
)
from PySide6.QtCore import Qt
from gui.MainContent.EpisodeDetailsPage import EpisodeDetailsPage
from gui.RatingWidgets.RatingWidget import RatingWidget

class SeasonDetailsPage(QWidget):
    def __init__(self, navigation_controller, api_manager, rating_manager, show, season_details):
        super().__init__()
        self.nav = navigation_controller
        self.api_manager = api_manager
        self.rating_manager = rating_manager
        self.show = show
        self.season_details = season_details

        layout = QVBoxLayout(self)

        name = show.get('name', 'Unknown Name')
        season_num = season_details.get('season_number', '?')
        air_date = season_details.get('air_date', 'Unknown Date')
        overview = season_details.get('overview', 'No overview available.')
        episodes = season_details.get('episodes', [])

        # Title
        show_label = QLabel(f"<h1>{name}</h1>")
        layout.addWidget(show_label)

        header_label = QLabel(f"<h2>Season {season_num}</h2>")
        header_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(header_label)

        # Air Date
        air_date_label = QLabel(f"<b>Air Date</b>: {air_date}")
        air_date_label.setAlignment(Qt.AlignLeft)
        layout.addWidget(air_date_label)

        # Overview
        overview_label = QLabel(overview)
        overview_label.setWordWrap(True)
        overview_label.setAlignment(Qt.AlignTop)

        overview_scroll = QScrollArea()
        overview_scroll.setWidget(overview_label)
        overview_scroll.setWidgetResizable(True)
        overview_scroll.setFixedHeight(80)
        layout.addWidget(overview_scroll)

        if episodes:
            episodes_label = QLabel("<h3>Episodes:</h3>")
            episodes_label.setAlignment(Qt.AlignLeft)
            layout.addWidget(episodes_label)

            scroll_area = QScrollArea()
            scroll_area.setWidgetResizable(True)
            scroll_content = QWidget()
            scroll_layout = QVBoxLayout(scroll_content)

            for ep in episodes:
                ep_num = ep.get('episode_number', '?')
                ep_name = ep.get('name', 'Unknown Episode')

                ep_button = QPushButton(f"Episode {ep_num}: {ep_name}")
                ep_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
                ep_button.clicked.connect(self._create_view_episode_handler(ep))
                scroll_layout.addWidget(ep_button)

            scroll_layout.addStretch()
            scroll_area.setWidget(scroll_content)
            layout.addWidget(scroll_area)

        # Create a pre-formatted ID for the season, e.g. "tv:12345-S2"
        content_id = f"tv:{show.get('id')}-S{season_num}"

        # Add the RatingWidget
        season_rating_widget = RatingWidget(
            parent=self,
            rating_manager=self.rating_manager,
            content_id=content_id, # "tv:12345-S2"
            title_text="Rate this Season"
        )
        layout.addWidget(season_rating_widget)

        layout.addStretch()

    def _create_view_episode_handler(self, episode):
        return lambda: self.view_episode(episode)

    def view_episode(self, episode):
        page = EpisodeDetailsPage(
            self.nav,
            self.api_manager,
            self.rating_manager,
            self.show,
            episode
        )
        self.nav.push(page)