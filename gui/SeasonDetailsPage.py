# gui/SeasonDetailsPage.py
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QScrollArea, QSizePolicy, QFrame
from PySide6.QtCore import Qt

class SeasonDetailsPage(QWidget):
    def __init__(self, navigation_controller, api_manager, show, season_details):
        super().__init__()
        self.nav = navigation_controller
        self.api_manager = api_manager
        self.show = show
        self.season_details = season_details

        # Main layout
        layout = QVBoxLayout()

        # Extract season details
        season_num = season_details.get('season_number', '?')
        air_date = season_details.get('air_date', 'Unknown Date')
        overview = season_details.get('overview', 'No overview available.')

        # Header Section
        header_label = QLabel(f"<h2>Season {season_num}</h2>")
        header_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(header_label)

        # Air Date Label
        air_date_label = QLabel(f"<b>Air Date</b>: {air_date}")
        air_date_label.setAlignment(Qt.AlignLeft)
        layout.addWidget(air_date_label)

        # Overview Section in a Scrollable Area
        overview_label = QLabel(f"{overview}")
        overview_label.setWordWrap(True)
        overview_label.setAlignment(Qt.AlignTop)

        overview_scroll = QScrollArea()
        overview_scroll.setWidget(overview_label)
        overview_scroll.setWidgetResizable(True)
        overview_scroll.setFixedHeight(100)  # Limit height for long overviews
        layout.addWidget(overview_scroll)

        # Episodes Section
        episodes = season_details.get('episodes', [])
        if episodes:
            episodes_label = QLabel("<h3>Episodes:</h3>")
            episodes_label.setAlignment(Qt.AlignLeft)
            layout.addWidget(episodes_label)

            # Scrollable area for episodes
            scroll_area = QScrollArea()
            scroll_area.setWidgetResizable(True)
            scroll_content = QWidget()
            scroll_layout = QVBoxLayout()

            # Dynamically add buttons for each episode
            for ep in episodes:
                ep_num = ep.get('episode_number', '?')
                ep_name = ep.get('name', 'Unknown Episode')

                # Episode Button
                ep_button = QPushButton(f"Episode {ep_num}: {ep_name}")
                ep_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)

                # Style buttons for better appearance
                ep_button.setStyleSheet("""
                    QPushButton {
                        text-align: left;
                        padding: 8px;
                        border: 1px solid #ccc;
                        border-radius: 5px;
                    }
                    QPushButton:hover {
                        background-color: #f0f0f0;
                    }
                """)

                ep_button.clicked.connect(self._create_view_episode_handler(ep))
                scroll_layout.addWidget(ep_button)

            scroll_layout.addStretch()  # Add spacing at the end
            scroll_content.setLayout(scroll_layout)
            scroll_area.setWidget(scroll_content)
            layout.addWidget(scroll_area)

        # Final Layout Setup
        layout.addStretch()  # Push content up for better alignment
        self.setLayout(layout)

    def _create_view_episode_handler(self, episode):
        """Helper method to handle episode button clicks."""
        return lambda: self.view_episode(episode)

    def view_episode(self, episode):
        """Navigate to the EpisodeDetailsPage for the selected episode."""
        from gui.EpisodeDetailsPage import EpisodeDetailsPage
        episode_page = EpisodeDetailsPage(self.nav, self.api_manager, self.show, episode)
        self.nav.push(episode_page)