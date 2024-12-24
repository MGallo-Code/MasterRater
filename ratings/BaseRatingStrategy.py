# ratings/BaseRatingStrategy.py

from abc import ABC, abstractmethod

class BaseRatingStrategy(ABC):
    """
    Abstract base class for rating strategies.
    Each subclass:
      - load_rating(rating_manager)
      - save_rating(rating_manager)
      - get_overall_rating()
      - remove_rating(rating_manager)
    """

    def __init__(self, content_id, content_type=None):
        """
        content_id: a pre-formatted unique string like "tv:12345-S2-E2" or "movie:200"
        content_type: optional string if you want to store the type (movie, tv, etc.)
        """
        self.content_id = content_id
        self.content_type = content_type

    @abstractmethod
    def load_rating(self, rating_manager):
        pass

    @abstractmethod
    def save_rating(self, rating_manager):
        pass

    @abstractmethod
    def get_overall_rating(self):
        pass

    @abstractmethod
    def remove_rating(self, rating_manager):
        pass