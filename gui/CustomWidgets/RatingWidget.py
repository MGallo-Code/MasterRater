# gui/RatingWidgets/RatingWidget.py
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QMessageBox
)
from PySide6.QtCore import Qt

from gui.CustomWidgets.MixedRatingDialog import MixedRatingDialog
from ratings.MixedRatingStrategy import MixedRatingStrategy

class RatingWidget(QWidget):
    """
    A reusable widget that displays + manages a MixedRatingStrategy rating 
    for a pre-formatted content_id (e.g. "tv:12345-S2").
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

        layout = QVBoxLayout(self)

        # Display user rating or "not rated"
        self.user_rating_label = QLabel()
        self.user_rating_label.setWordWrap(True)
        layout.addWidget(self.user_rating_label)

        # "Rate" Button -> opens MixedRatingDialog
        self.rate_button = QPushButton(self.title_text)
        self.rate_button.clicked.connect(self.open_rating_dialog)
        layout.addWidget(self.rate_button)

        # Remove Rating Button
        self.remove_rating_button = QPushButton("Remove Rating")
        self.remove_rating_button.clicked.connect(self.remove_rating)
        layout.addWidget(self.remove_rating_button)

        self.refresh_content()

    def refresh_content(self):
        """
        Load the MixedRatingStrategy from rating_manager, then update the label.
        """
        strategy = MixedRatingStrategy(self.content_id, self.content_type)
        strategy.load_rating(self.rating_manager)

        overall = strategy.get_overall_rating()
        # Check if no single rating and no categories => not rated
        if (overall is None and 
            not any(info[1] is not None for info in strategy.categories.values())):
            self.user_rating_label.setText("You haven't rated this content yet.")
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

            # Category breakdown
            any_category = False
            for cat_key, info in strategy.categories.items():
                name, value, weight = info
                if value is not None:
                    any_category = True
                    lines.append(f"{name}: {value} (Weight {weight}x)")

            if not any_category:
                lines.append("No category scores have been entered yet.")

            self.user_rating_label.setText("\n".join(lines))
            self.remove_rating_button.setVisible(True)

    def open_rating_dialog(self):
        dialog = MixedRatingDialog(
            parent=self,
            rating_manager=self.rating_manager,
            content_id=self.content_id,
            content_type=self.content_type
        )
        if dialog.exec():
            self.refresh_content()

    def remove_rating(self):
        confirm = QMessageBox.question(
            self,
            "Confirm Removal",
            "Are you sure you want to remove this rating?",
            QMessageBox.Yes | QMessageBox.No
        )
        if confirm == QMessageBox.Yes:
            strategy = MixedRatingStrategy(self.content_id, self.content_type)
            strategy.remove_rating(self.rating_manager)
            self.refresh_content()