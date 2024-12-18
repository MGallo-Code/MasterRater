# gui/ShowDetailsPage.py
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QScrollArea, QSizePolicy
from gui.SeasonDetailsPage import SeasonDetailsPage

class ShowDetailsPage(QWidget):
    def __init__(self, navigation_controller, api_manager, show):
        super().__init__()
        self.nav = navigation_controller
        self.api_manager = api_manager
        self.show = show

        # Main layout
        layout = QVBoxLayout()

        # Extract show details
        name = show.get('name', 'Unknown Name')
        first_air_date = show.get('first_air_date', 'Unknown Date')
        num_seasons = show.get('number_of_seasons', 0)
        overview = show.get('overview', 'No overview available.')
        rating = show.get('vote_average', 'No rating available.')

        # Header labels
        layout.addWidget(QLabel(f"<h2>{name}</h2>"))
        layout.addWidget(QLabel(f"First Air Date: {first_air_date}"))
        layout.addWidget(QLabel(f"Rating: {rating}"))

        # Overview with word wrapping in a scrollable area
        overview_label = QLabel(f"{overview}")
        overview_label.setWordWrap(True)
        overview_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)

        overview_scroll = QScrollArea()
        overview_scroll.setWidget(overview_label)
        overview_scroll.setWidgetResizable(True)
        overview_scroll.setFixedHeight(100)
        layout.addWidget(overview_scroll)

        # Seasons Section
        if num_seasons > 0:
            layout.addWidget(QLabel("<b>Seasons:</b>"))

            # Scrollable area for seasons
            scroll_area = QScrollArea()
            scroll_area.setWidgetResizable(True)
            scroll_content = QWidget()
            scroll_layout = QVBoxLayout()

            # Dynamically add buttons for each season
            for season_number in range(1, num_seasons + 1):
                season_btn = QPushButton(f"Season {season_number}")
                season_btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
                season_btn.clicked.connect(self._create_view_season_handler(season_number))
                scroll_layout.addWidget(season_btn)

            # Add spacing
            scroll_layout.addStretch()
            scroll_content.setLayout(scroll_layout)
            scroll_area.setWidget(scroll_content)
            layout.addWidget(scroll_area)

        # Rate Button
        rate_button = QPushButton("Rate this Show")
        rate_button.clicked.connect(self.open_rating_dialog)
        layout.addWidget(rate_button)

        self.setLayout(layout)

    def _create_view_season_handler(self, season_number):
        """Helper to create season button handlers."""
        return lambda: self.view_season(season_number)

    def view_season(self, season_number):
        """Fetch season details and navigate to SeasonDetailsPage."""
        season_details = self.api_manager.get_season_details(str(self.show['id']), season_number)
        season_details_page = SeasonDetailsPage(self.nav, self.api_manager, self.show, season_details)
        self.nav.push(season_details_page)

    def open_rating_dialog(self):
        # Placeholder for rating logic
        print("Opening rating dialog...")