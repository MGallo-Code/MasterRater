# gui/RatingWidgets/RatingWidget.py
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QLineEdit, QHBoxLayout, QMessageBox
)
from PySide6.QtCore import Qt

from gui.RatingWidgets.MixedRatingDialog import MixedRatingDialog
from ratings.BaseRatingStrategy import MixedRatingStrategy

class RatingWidget(QWidget):
    """
    A reusable widget that displays the current rating for a given content (movie, episode, etc.)
    using a MixedRatingStrategy. The user can open a dialog to input either
    a single rating or category ratings. If a single rating is given, that acts
    like an 'override'; otherwise the category average is used.
    """

    def __init__(
        self,
        parent,
        rating_manager,
        content_id,
        content_type="movie",
        title_text="Rate this Content"
    ):
        super().__init__(parent)
        self.rating_manager = rating_manager
        self.content_id = content_id
        self.content_type = content_type
        self.title_text = title_text

        self.layout = QVBoxLayout(self)
        self.setup_ui()
        self.refresh_content()

    def setup_ui(self):
        # Display user rating or "not rated"
        self.user_rating_label = QLabel()
        self.user_rating_label.setWordWrap(True)
        self.layout.addWidget(self.user_rating_label)

        # "Rate" Button -> opens MixedRatingDialog
        self.rate_button = QPushButton(self.title_text)
        self.rate_button.clicked.connect(self.open_rating_dialog)
        self.layout.addWidget(self.rate_button)

        # Single rating is effectively the "override" in MixedRatingStrategy
        self.override_widget = QWidget()

        self.layout.addWidget(self.override_widget)

        # Remove Rating Button
        self.remove_rating_button = QPushButton("Remove Rating")
        self.remove_rating_button.clicked.connect(self.remove_rating)
        self.layout.addWidget(self.remove_rating_button)

    def refresh_content(self):
        """
        Re-load the MixedRatingStrategy from rating_manager, then update UI
        to reflect single rating (if any), category average, etc.
        """
        strategy = MixedRatingStrategy(self.content_id)
        strategy.load_rating(self.rating_manager)

        overall = strategy.get_overall_rating()
        if overall is None and not any(
            cat_info[1] is not None for cat_info in strategy.categories.values()
        ):
            # No single rating, no categories => Not rated
            self.user_rating_label.setText("You haven't rated this content yet.")
            self.override_widget.setVisible(False)
            self.remove_rating_button.setVisible(False)
        else:
            lines = []
            if strategy.one_score is not None:
                lines.append(f"Overall Rating: {strategy.one_score} (Single Score)")
            else:
                if strategy.total_rating is not None:
                    lines.append(f"Overall Rating: {strategy.total_rating} (Calculated from categories)")
                else:
                    lines.append("Overall Rating: None (Calculated from categories)")

            # Show category breakdown if any
            any_category = False
            for cat_key, info in strategy.categories.items():
                cat_name, value, weight = info
                if value is not None:
                    any_category = True
                    lines.append(f"{cat_name}: {value} (Weight {weight}x)")

            if not any_category:
                lines.append("No category scores have been entered yet.")

            self.user_rating_label.setText("\n".join(lines))

            self.override_widget.setVisible(True)
            self.remove_rating_button.setVisible(True)

    def open_rating_dialog(self):
        """
        Open the MixedRatingDialog. The user can specify a single rating,
        categories, or both. Once done, we refresh.
        """
        dialog = MixedRatingDialog(
            parent=self,
            rating_manager=self.rating_manager,
            content_id=self.content_id,
            content_type=self.content_type
        )
        if dialog.exec():
            self.refresh_content()

    def remove_rating(self):
        """
        Prompt user, then remove rating entirely from rating_manager.
        """
        from PySide6.QtWidgets import QMessageBox
        confirm = QMessageBox.question(
            self,
            "Confirm Removal",
            "Are you sure you want to remove this rating?",
            QMessageBox.Yes | QMessageBox.No
        )
        if confirm == QMessageBox.Yes:
            strategy = MixedRatingStrategy(self.content_id)
            strategy.remove_rating(self.rating_manager)
            self.refresh_content()