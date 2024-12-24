# gui/RatingWidgets/RatingDialog.py

from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QFormLayout
from ratings.Rating import Rating

class RatingDialog(QDialog):
    def __init__(self, parent, rating_manager, content_id, content_type="movie", season_number=None, episode_number=None):
        super().__init__(parent)

        self.setWindowTitle("Rate Content")
        self.rating_manager = rating_manager
        self.content_id = content_id
        self.content_type = content_type
        self.season_number = season_number
        self.episode_number = episode_number

        # Load existing rating or create a new one
        self.rating = self.rating_manager.get_rating(content_id) or Rating(content_id, content_type, season_number, episode_number)

        # Layout
        self.layout = QVBoxLayout()

        # Header
        self.layout.addWidget(QLabel(f"<h2>Rate {content_type.title()}</h2>"))

        # Form for rating categories
        self.form_layout = QFormLayout()
        self.inputs = {}
        for category_key, category_info in self.rating.ratings.items():
            label = category_info[0]
            input_field = QLineEdit()
            input_field.setPlaceholderText("Enter rating or leave blank to skip")
            if category_info[1] is not None:
                input_field.setText(str(category_info[1]))
            self.inputs[category_key] = input_field
            self.form_layout.addRow(QLabel(label), input_field)
        self.layout.addLayout(self.form_layout)

        # Save button
        self.save_button = QPushButton("Save Ratings")
        self.save_button.clicked.connect(self.save_ratings)
        self.layout.addWidget(self.save_button)

        # Cancel button
        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.clicked.connect(self.reject)
        self.layout.addWidget(self.cancel_button)

        self.setLayout(self.layout)

    def save_ratings(self):
        # Update ratings based on user input
        for category_key, input_field in self.inputs.items():
            value = input_field.text()
            if value.strip():
                try:
                    self.rating.update_rating(category_key, float(value))
                except ValueError:
                    print(f"ERROR HANDLING INPUT:\ncategory_key: {str(category_key)}\ninput_field: {str(input_field)}")
                    pass  # Ignore invalid inputs (e.g., non-numeric)

        # Save the rating
        self.rating.save(self.rating_manager)

        # Refresh the parent window's content
        self.parent().refresh_content()

        # Close the dialog
        self.accept()