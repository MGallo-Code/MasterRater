# gui/MainContent/ShowDetailsPage.py

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QScrollArea, QSizePolicy
)
from PySide6.QtCore import Qt
from gui.MainContent.SeasonDetailsPage import SeasonDetailsPage
from gui.RatingWidgets.MixedRatingDialog import MixedRatingDialog

class ShowDetailsPage(QWidget):
    def __init__(self, navigation_controller, api_manager, rating_manager, show):
        super().__init__()
        self.nav = navigation_controller
        self.api_manager = api_manager
        self.rating_manager = rating_manager
        self.show = show

        layout = QVBoxLayout()
        self.setLayout(layout)

        # Show info
        name = show.get('name', 'Unknown Name')
        first_air_date = show.get('first_air_date', 'Unknown Date')
        num_seasons = show.get('number_of_seasons', 0)
        overview = show.get('overview', 'No overview available.')
        global_rating = show.get('vote_average', 'No rating available.')

        # Title
        title_label = QLabel(f"<h2>{name}</h2>")
        title_label.setTextFormat(Qt.RichText)
        layout.addWidget(title_label)

        layout.addWidget(QLabel(f"First Air Date: {first_air_date}"))
        layout.addWidget(QLabel(f"TMDB Global Rating: {global_rating}"))

        # Overview in a scroll area
        overview_label = QLabel(overview)
        overview_label.setWordWrap(True)
        overview_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)

        overview_scroll = QScrollArea()
        overview_scroll.setWidget(overview_label)
        overview_scroll.setWidgetResizable(True)
        overview_scroll.setFixedHeight(100)
        layout.addWidget(overview_scroll)

        # Seasons
        if num_seasons > 0:
            layout.addWidget(QLabel("<b>Seasons:</b>"))

            scroll_area = QScrollArea()
            scroll_area.setWidgetResizable(True)
            scroll_content = QWidget()
            scroll_layout = QVBoxLayout()

            for season_number in range(1, num_seasons + 1):
                season_btn = QPushButton(f"Season {season_number}")
                season_btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
                # Late-binding fix: pass season_number as default param
                season_btn.clicked.connect(lambda _, sn=season_number: self.view_season(sn))
                scroll_layout.addWidget(season_btn)

            scroll_layout.addStretch()
            scroll_content.setLayout(scroll_layout)
            scroll_area.setWidget(scroll_content)
            layout.addWidget(scroll_area)

        # Rate Button -> open rating dialog for the entire show
        rate_button = QPushButton("Rate this Show")
        rate_button.clicked.connect(self.open_rating_dialog)
        layout.addWidget(rate_button)

    def view_season(self, season_number):
        """
        Fetch season details and navigate to SeasonDetailsPage.
        """
        season_details = self.api_manager.get_season_details(str(self.show['id']), season_number)
        season_details_page = SeasonDetailsPage(
            self.nav, self.api_manager, self.rating_manager, self.show, season_details
        )
        self.nav.push(season_details_page)

    def open_rating_dialog(self):
        """
        Example: Opens a MixedRatingDialog for rating the entire show as a whole.
        The content_id can be just str(show['id']) or any custom scheme.
        """
        content_id = str(self.show['id'])
        dialog = MixedRatingDialog(
            parent=self,
            rating_manager=self.rating_manager,
            content_id=content_id,
            content_type="tv"  # or "show"
        )
        if dialog.exec():
            # Optionally refresh some part of UI if we want to display the rating
            pass