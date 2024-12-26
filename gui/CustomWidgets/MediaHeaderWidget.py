# gui/CustomWidgets/MediaHeaderWidget.py

import requests
from PySide6.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QMainWindow, QSizePolicy
)
from PySide6.QtCore import Qt, QRect
from PySide6.QtGui import QPixmap, QPainter, QLinearGradient, QColor

class MediaHeaderWidget(QWidget):
    """
    A custom widget that displays:
      - A cropped/faded backdrop at the top
      - A poster on the left, overlapping the backdrop, with a border + round corners
      - A title label with a translucent background, also overlapping the backdrop

    The backdrop's width matches this widget's width,
    and the height is a fraction (e.g. 0.3) of the parent widget's height.
    Then we fade the bottom portion to white (via existing fade_to_white).
    """

    def __init__(
        self,
        parent=None,
        title="Untitled",
        backdrop_path=None,
        poster_path=None,
        # The fraction of parent's height we want
        # e.g. 0.4 means the backdrop is 40% of parent's height
        backdrop_height_fraction=0.4,
        # Fraction of content window's height we want poster to be
        poster_height_fraction=0.45,

        poster_offset=(45, 30),
        # Where fade begins (0.6 means 60% down the final cropped portion)
        fade_start_fraction=0.6,
    ):
        super().__init__(parent)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.title = title
        self.backdrop_path = backdrop_path
        self.poster_path = poster_path
        self.backdrop_height_fraction = backdrop_height_fraction
        self.poster_height_fraction = poster_height_fraction
        self.poster_offset = poster_offset
        self.fade_start_fraction = fade_start_fraction

        # We'll store the original backdrop as a QPixmap here
        self.backdrop_original = None
        self.poster_original = None

        # Backdrop Label
        self.backdrop_label = QLabel(self)
        self.backdrop_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.backdrop_label.setStyleSheet("padding:0;")

        # Poster label
        self.poster_label = QLabel(self)
        self.poster_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.poster_label.setStyleSheet("""
            QLabel {
                border: 3px solid #000;
                border-radius: 5px;
                padding:0; margin:0;
            }
        """)

        # Title label
        self.title_label = QLabel(f"<h1>{self.title}</h1>", self)
        self.title_label.setWordWrap(True)
        self.title_label.setStyleSheet("""
            QLabel {
                text-align: center;
                background-color: transparent;
                color: black;
                padding: 12px 18px;
                border-radius: 5px;
                margin:0;
                font-size: 6rem;
            }
        """)

        # Load images
        self.load_backdrop()
        self.load_poster()

        self.update()

    def update_size_values(self):
        # Retrieve MainWindow
        main_window = self.window()  # This gives the top-level MainWindow
        if not isinstance(main_window, QMainWindow):
            main_window = self.parent()  # Fallback to the immediate parent if window() isn't QMainWindow

        # Get content area size
        self.current_window_width = main_window.width()
        self.current_window_height = main_window.height()

        # Get corresponding poster/backdrop heights
        self.desired_poster_height = int(self.current_window_height * self.poster_height_fraction) if self.poster_original else 0
        self.desired_backdrop_height = int(self.current_window_height * self.backdrop_height_fraction) if self.backdrop_original else 0

        # Header's height should be largest height between backdrop and (poster+padding[y value])
        self.desired_header_height = max(self.desired_poster_height + self.poster_offset[1] * 2, self.desired_backdrop_height)

    def update(self):
        # Update height values (dependent on content area height)
        self.update_size_values()
        # Ensure header is set to minimum required height
        self.setMinimumHeight(self.desired_header_height)
        # Update backdrop and poster labels
        self.update_backdrop_label()
        self.update_poster_label()
        # Position poster and title overlays
        self.position_overlay()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.update()
    
    def showEvent(self, event):
        super().showEvent(event)
        self.update()

    def position_overlay(self):
        """Absolute positioning for poster + title over the backdrop."""

        # Poster's offset
        x_offset = self.poster_offset[0] if self.poster_original else 0
        y_offset = self.poster_offset[1] if self.poster_original else 0
        poster_width = self.desired_poster_width if self.poster_original else 0
        # If poster exists, position it.
        if self.poster_original:
            # Set poster geometry
            self.poster_label.setGeometry(x_offset, y_offset, poster_width, self.desired_poster_height)

        # Title geometry
        self.title_label.adjustSize()
        title_x = poster_width + x_offset + x_offset
        title_y = self.height() - self.title_label.height()
        self.title_label.setGeometry(title_x, title_y, self.current_window_width - x_offset - title_x, self.title_label.height())

    # ~~~~~~~~~~~~~~~~~~ Backdrop Logic ~~~~~~~~~~~~~~~~~~ #
    def load_backdrop(self):
        """
        We'll only fetch the original once here, store in self.backdrop_original,
        and do no scaling/cropping yet. We'll do that dynamically on resize.
        """
        if not self.backdrop_path:
            return
        pm = self.fetch_image(self.backdrop_path, size_key="w1280")
        if pm:
            self.backdrop_original = pm

    def update_backdrop_label(self):
        """
        Dynamically scale, crop, and fade the original backdrop based on the widget's size.
        Uses the MainWindow size instead of the immediate parent widget.
        """
        if not self.backdrop_original:
            return

        # Scale the original image to fit the current width
        scaled = self.backdrop_original.scaledToWidth(self.current_window_width, Qt.SmoothTransformation)

        # Crop the top portion to the desired height
        final_h = min(scaled.height(), self.desired_backdrop_height)
        cropped = scaled.copy(0, 0, scaled.width(), final_h)

        # Apply fading to the bottom portion
        faded = self.fade_to_white(cropped, self.fade_start_fraction)

        # Set the final pixmap
        self.backdrop_label.setGeometry(0, 0, self.current_window_width, final_h)
        self.backdrop_label.setPixmap(faded)

    # ~~~~~~~~~~~~~~~~~~ Poster Logic ~~~~~~~~~~~~~~~~~~ #
    def load_poster(self):
        if not self.poster_path:
            return
        pm = self.fetch_image(self.poster_path, size_key="w342")
        if pm:
            self.poster_original = pm
    
    def update_poster_label(self):
        """
        Scale the original poster to:
          - height = backdrop's height * self.poster_height_fraction
        Then set the result on self.poster_label
        """
        if not self.poster_original:
            self.desired_poster_width = 0
            return

        # Scale poster, set
        scaled = self.poster_original.scaledToHeight(self.desired_poster_height, Qt.SmoothTransformation)
        self.poster_label.setPixmap(scaled)

        self.desired_poster_width = scaled.width()

    # ~~~~~~~~~~~~~~~~~~ Fetchers ~~~~~~~~~~~~~~~~~~ #
    def fetch_image(self, path, size_key="w500"):
        if not path:
            return None
        url = f"https://image.tmdb.org/t/p/{size_key}{path}"
        try:
            resp = requests.get(url, timeout=5)
            resp.raise_for_status()
            pm = QPixmap()
            if pm.loadFromData(resp.content):
                return pm
        except Exception as e:
            print("Image fetch error:", e)
        return None

    # ~~~~~~~~~~~~~~~~~~ fade_to_white (unchanged) ~~~~~~~~~~~~~~~~~~ #
    def fade_to_white(self, pixmap, start_fraction=0.8):
        """
        DO NOT MODIFY THIS LOGIC
        Fades the bottom portion of 'pixmap' to solid white with a
        multi-stop gradient. 
        """
        if pixmap.isNull():
            return pixmap

        w = pixmap.width()
        h = pixmap.height()
        start_y = int(h * start_fraction)
        if start_y < 0:
            start_y = 0
        if start_y >= h:
            return pixmap

        faded = QPixmap(w, h)
        faded.fill(Qt.transparent)

        painter = QPainter(faded)
        painter.drawPixmap(0, 0, pixmap)
        painter.setCompositionMode(QPainter.CompositionMode_SourceOver)

        gradient = QLinearGradient(0, float(start_y), 0, float(h))
        bg_color = QColor(249, 249, 249, 0)
        gradient.setColorAt(0.00, bg_color)
        bg_color.setAlpha(60)
        gradient.setColorAt(0.20, bg_color)
        bg_color.setAlpha(90)
        gradient.setColorAt(0.30, bg_color)
        bg_color.setAlpha(130)
        gradient.setColorAt(0.50, bg_color)
        bg_color.setAlpha(230)
        gradient.setColorAt(0.80, bg_color)
        bg_color.setAlpha(247)
        gradient.setColorAt(0.90, bg_color)
        bg_color.setAlpha(255) 
        gradient.setColorAt(1.00, bg_color)

        painter.fillRect(QRect(0, start_y, w, h - start_y), gradient)
        painter.end()
        return faded