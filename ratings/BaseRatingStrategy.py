# ratings/BaseRatingStrategy.py

import math
from abc import ABC, abstractmethod

class BaseRatingStrategy(ABC):
    """
    Abstract base class for rating strategies.
    """

    def __init__(self, content_id):
        self.content_id = content_id

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


class MixedRatingStrategy(BaseRatingStrategy):
    """
    A 'unified' strategy that can store either/both:
        1) A single numeric rating (one_score), e.g., 8.5
        2) Categorical ratings (like Plot, Acting, etc.)

    If one_score is not None, that is taken as the overall rating.
    Otherwise, the categories are used to compute an average.
    """

    def __init__(self, content_id):
        super().__init__(content_id)
        # Single rating number (if user only wants one score)
        self.one_score = None

        # A dictionary of categories:
        #   key -> [display_name, rating_value, weight]
        self.categories = {
            "plot_rating": ["Plot Rating", None, 1],
            "aesthetic_rating": ["Aesthetic Rating", None, 1],
            "immersion_rating": ["Immersion Rating", None, 1],
            # ... add more as you like
        }
        self.total_rating = None  # Calculated from categories if one_score is None

    def load_rating(self, rating_manager):
        data = rating_manager.get_rating_data(self.content_id)
        if data:
            # If user previously stored one_score
            self.one_score = data.get("one_score")
            # If user previously stored category info
            self.categories = data.get("categories", self.categories)
            # If user previously stored a cached total (not strictly required)
            self.total_rating = data.get("total_rating")

    def save_rating(self, rating_manager):
        """
        If one_score is None, we recalc total_rating from categories.
        If one_score is not None, that is effectively the overall rating 
        (we still might store total_rating from categories for reference).
        """
        self._calculate_total_rating()

        rating_data = {
            "strategy_type": "mixed",
            "one_score": self.one_score,         # The optional single numeric rating
            "categories": self.categories,       # The dictionary of category ratings
            "total_rating": self.total_rating    # The last computed category average
        }
        rating_manager.save_rating_data(self.content_id, rating_data)

    def _calculate_total_rating(self):
        """
        Compute a weighted average from categories, storing in self.total_rating.
        If no categories have a value, it becomes None.
        """
        weighted_sum = 0
        total_weight = 0
        for cat_key, info in self.categories.items():
            rating_value = info[1]
            weight = info[2]
            if rating_value is not None:
                weighted_sum += rating_value * weight
                total_weight += weight

        if total_weight > 0:
            self.total_rating = weighted_sum / total_weight
        else:
            self.total_rating = None

    def get_overall_rating(self):
        """
        If self.one_score is not None, that is the overall rating.
        Otherwise, we return self.total_rating from the categories.
        """
        if self.one_score is not None:
            return self.one_score
        return self.total_rating

    def remove_rating(self, rating_manager):
        rating_manager.delete_rating_data(self.content_id)
        self.one_score = None
        self.categories = {}
        self.total_rating = None