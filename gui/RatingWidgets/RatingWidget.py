# gui/RatingWidgets/RatingWidget.py
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QLineEdit, QHBoxLayout, QMessageBox
)
from PySide6.QtCore import Qt
from gui.RatingWidgets.RatingDialog import RatingDialog

class RatingWidget(QWidget):
    """
    A reusable widget that displays the current rating for a given content (movie, episode, etc.)
    and provides override, remove, and 'open rating dialog' functionality.
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

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # Label showing user rating or "not rated" text
        self.user_rating_label = QLabel()
        self.user_rating_label.setWordWrap(True)
        self.layout.addWidget(self.user_rating_label)

        # Rate Button
        self.rate_button = QPushButton(self.title_text)
        self.rate_button.clicked.connect(self.open_rating_dialog)
        self.layout.addWidget(self.rate_button)

        # Override / Remove Section
        self.override_widget = QWidget()
        override_layout = QHBoxLayout(self.override_widget)

        self.override_input = QLineEdit()
        self.override_input.setPlaceholderText("Enter override (e.g. 8.5)")
        override_layout.addWidget(self.override_input)

        self.apply_override_button = QPushButton("Apply Override")
        self.apply_override_button.clicked.connect(self.apply_override)
        override_layout.addWidget(self.apply_override_button)

        self.clear_override_button = QPushButton("Clear Override")
        self.clear_override_button.clicked.connect(self.clear_override)
        override_layout.addWidget(self.clear_override_button)

        self.layout.addWidget(self.override_widget)

        self.remove_rating_button = QPushButton("Remove Rating")
        self.remove_rating_button.clicked.connect(self.remove_rating)
        self.layout.addWidget(self.remove_rating_button)

        self.refresh_content()

    def refresh_content(self):
        """
        Refresh the UI based on whether a rating exists and whether it has override
        or category details.
        """
        rating_obj = self.get_rating_object()

        if not rating_obj:
            self.user_rating_label.setText("You haven't rated this content yet.")
            self.override_widget.setVisible(False)
            self.remove_rating_button.setVisible(False)
        else:
            # Show overall rating (override or calculated)
            lines = []
            if rating_obj.total_rating_override is not None:
                lines.append(f"Overall Rating: {rating_obj.total_rating_override} (Overridden)")
            else:
                if rating_obj.total_rating is not None:
                    lines.append(f"Overall Rating: {rating_obj.total_rating} (Calculated)")
                else:
                    lines.append("Overall Rating: None (Calculated)")

            # Show category breakdown if any
            any_categories = False
            for key, info in rating_obj.ratings.items():
                category_name, value, weight = info
                if value is not None:
                    any_categories = True
                    lines.append(f"{category_name}: {value} (Weight {weight}x)")

            if not any_categories:
                lines.append("No category scores have been entered yet.")

            self.user_rating_label.setText("\n".join(lines))

            self.override_widget.setVisible(True)
            self.remove_rating_button.setVisible(True)

    def get_rating_object(self):
        """
        Fetch the rating from the manager; return None if it doesn't exist.
        """
        return self.rating_manager.get_rating(self.content_id)

    def open_rating_dialog(self):
        """
        Open the rating dialog. The dialog handles creation or update of the rating.
        """
        dialog = RatingDialog(
            parent=self,
            rating_manager=self.rating_manager,
            content_id=self.content_id,
            content_type=self.content_type,
        )
        if dialog.exec():
            # If user accepted changes, refresh
            self.refresh_content()

    def apply_override(self):
        """
        Set an override rating if a rating object exists.
        """
        rating_obj = self.get_rating_object()
        if not rating_obj:
            return
        try:
            override_value = float(self.override_input.text().strip())
            rating_obj.total_rating_override = override_value
            self.rating_manager.add_or_update_rating(rating_obj)
            self.refresh_content()
        except ValueError:
            print("Invalid override input.")

    def clear_override(self):
        """
        Clear the override rating (if rating exists).
        """
        rating_obj = self.get_rating_object()
        if rating_obj:
            rating_obj.total_rating_override = None
            self.rating_manager.add_or_update_rating(rating_obj)
            self.refresh_content()

    def remove_rating(self):
        """
        Prompt user to confirm removal, then remove rating from manager.
        """
        rating_obj = self.get_rating_object()
        if not rating_obj:
            return

        from PySide6.QtWidgets import QMessageBox
        confirm = QMessageBox.question(
            self,
            "Confirm Removal",
            "Are you sure you want to remove this rating?",
            QMessageBox.Yes | QMessageBox.No
        )
        if confirm == QMessageBox.Yes:
            self.rating_manager.delete_rating(self.content_id)
            self.refresh_content()