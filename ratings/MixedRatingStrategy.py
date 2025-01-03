# ratings/MixedRatingStrategy.py

from ratings.BaseRatingStrategy import BaseRatingStrategy

class MixedRatingStrategy(BaseRatingStrategy):
    """
    Stores either a single numeric rating (self.one_score) or category-based ratings (self.categories).
    If one_score is not None, that "wins" as the overall rating. Otherwise, we compute from categories.
    """

    def __init__(self, content_id, content_type=None):
        super().__init__(content_id, content_type)
        self.one_score = None
        self.categories = {
            "plot_rating": ["Plot Rating", None, 1],
            "aesthetic_rating": ["Aesthetic Rating", None, 1],
            "immersion_rating": ["Immersion Rating", None, 1],
            # add more categories as needed...
        }
        self.total_rating = None

    def load_rating(self, rating_manager):
        data = rating_manager.get_rating_data(self.content_id)
        if data:
            self.one_score = data.get("one_score")
            self.categories = data.get("categories", self.categories)
            self.total_rating = data.get("total_rating")

    def save_rating(self, rating_manager):
        # Recompute total_rating from categories if one_score is None
        self._calculate_total_rating()

        rating_data = {
            "strategy_type": "mixed",
            "one_score": self.one_score,
            "categories": self.categories,
            "total_rating": self.total_rating
        }
        rating_manager.save_rating_data(self.content_id, rating_data)

    def _calculate_total_rating(self):
        weighted_sum = 0
        total_weight = 0
        for cat_key, info in self.categories.items():
            val, weight = info[1], info[2]
            if val is not None:
                weighted_sum += val * weight
                total_weight += weight
        self.total_rating = round(weighted_sum / total_weight, 3) if total_weight > 0 else None

    def get_overall_rating(self):
        """Single rating (self.one_score) takes precedence; otherwise category-based average."""
        return self.one_score if self.one_score is not None else self.total_rating

    def remove_rating(self, rating_manager):
        rating_manager.delete_rating_data(self.content_id)
        self.one_score = None
        self.categories = {}
        self.total_rating = None