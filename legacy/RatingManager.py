# legacy/RatingManager.py

import numpy as np

class RatingManager:
    def __init__(self, file_path="./data/saved_ratings.npy"):
        self.file_path = file_path
        self.ratings = self.load_ratings()

    def load_ratings(self):
        try:
            return np.load(self.file_path, allow_pickle=True).item()
        except FileNotFoundError:
            return {}

    def save_ratings(self):
        np.save(self.file_path, self.ratings, allow_pickle=True)

    def get_rating(self, content_id):
        return self.ratings.get(content_id)

    def add_or_update_rating(self, rating):
        # Add a new rating or update an existing rating in the manager.
        self.ratings[rating.content_id] = rating
        self.save_ratings()

    def delete_rating(self, content_id):
        # Delete a rating by content ID if it exists.
        if content_id in self.ratings:
            del self.ratings[content_id]
            self.save_ratings()