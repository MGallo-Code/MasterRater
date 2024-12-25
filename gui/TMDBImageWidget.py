# gui/Widgets/ImageWidget.py

import requests
from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt

class TMDBImageWidget(QWidget):
    """
    A custom widget that downloads and displays an image from TMDB or any URL.
    Optionally limit the displayed size (width/height) while preserving aspect ratio.
    """

    BASE_IMAGE_URL = "https://image.tmdb.org/t/p/"

    def __init__(
        self,
        parent=None,
        img_path=None,
        size_key="original",
        max_width=None,
        max_height=None
    ):
        """
        :param parent: parent widget
        :param poster_path: e.g. "/4edFyasCrkH4MKs6H4mHqlrxA6b.jpg"
        :param size_key: e.g. "original", "w500", "w300", etc.
        :param max_width: optional max width in pixels
        :param max_height: optional max height in pixels
        """
        super().__init__(parent)
        self.img_path = img_path
        self.size_key = size_key
        self.max_width = max_width
        self.max_height = max_height

        # Main layout
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)

        # Create a label to show the image or messages
        self.image_label = QLabel("No image loaded", self)
        self.image_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.image_label)

        # If user gave a poster path, load the image
        if self.img_path:
            self.load_and_display_image(self.img_path)

    def build_tmdb_image_url(self, img_path):
        """
        Construct the TMDB image URL from the poster path and the size key.
        e.g.: "https://image.tmdb.org/t/p/w500/img_path"
        """
        return f"{self.BASE_IMAGE_URL}{self.size_key}{img_path}"

    def load_and_display_image(self, img_path):
        """
        Download + display the image. Optionally apply max_width/max_height with aspect ratio.
        """
        url = self.build_tmdb_image_url(img_path)
        try:
            response = requests.get(url)
            response.raise_for_status()
            image_data = response.content

            pixmap = QPixmap()
            if not pixmap.loadFromData(image_data):
                self.image_label.setText("Failed to load image data.")
                return

            # If user wants to limit size
            if self.max_width or self.max_height:
                # Use current pixmap size as fallback if max_* is None
                orig_w = pixmap.width()
                orig_h = pixmap.height()

                limit_w = self.max_width if self.max_width else orig_w
                limit_h = self.max_height if self.max_height else orig_h

                scaled_pixmap = pixmap.scaled(
                    limit_w,
                    limit_h,
                    Qt.KeepAspectRatio,
                    Qt.SmoothTransformation
                )
                self.image_label.setPixmap(scaled_pixmap)
            else:
                # Just use original pixmap
                self.image_label.setPixmap(pixmap)

            self.image_label.adjustSize()

        except Exception as e:
            self.image_label.setText(f"Error fetching image:\n{e}")