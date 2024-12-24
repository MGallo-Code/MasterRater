# ratings/RatingManager.py
import numpy as np

class RatingManager:
    """
    A rating manager that loads/saves rating data as dictionaries,
    letting your rating strategy interpret that data.
    """

    def __init__(self, file_path="./data/saved_ratings.npy"):
        self.file_path = file_path
        self.rating_data_store = self._load_data()

    def _load_data(self):
        try:
            return np.load(self.file_path, allow_pickle=True).item()
        except FileNotFoundError:
            return {}

    def _save_data(self):
        np.save(self.file_path, self.rating_data_store, allow_pickle=True)

    def get_rating_data(self, content_id):
        """
        Return the raw dictionary for this content_id, or None if not found.
        """
        return self.rating_data_store.get(content_id)

    def save_rating_data(self, content_id, data_dict):
        """
        Save/update the dictionary for this content_id, then persist.
        """
        self.rating_data_store[content_id] = data_dict
        self._save_data()

    def delete_rating_data(self, content_id):
        """
        Remove the rating dictionary for content_id if it exists, and persist changes.
        """
        if content_id in self.rating_data_store:
            del self.rating_data_store[content_id]
            self._save_data()