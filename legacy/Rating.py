# legacy_ratings/Rating.py

class Rating:
    def __init__(self, content_id, content_type="movie", season_number=None, episode_number=None):
        # Represents show or movie ID in string format
        self.content_id = content_id
        # Type of content, i.e. "movie" or "tv"
        self.content_type = content_type
        # Season number, if applicable
        self.season_number = season_number
        # Episode number, if present
        self.episode_number = episode_number
        # TODO: confirm content exists

        # Default ratings (Rating Category Name, Rating Value, Weight)
        #  (X, None, 1) is default, unrated
        self.ratings = {
            "plot_rating": ["Plot Rating", None, 1],
            "aesthetic_rating": ["Aesthetic Rating", None, 1],
            "immersion_rating": ["Immersion Rating", None, 1],
            "charm_rating": ["Charm Rating", None, 1],
            "humor_rating": ["Humor Rating", None, 1],
            "horror_rating": ["Horror Rating", None, 1],
            "dialogue_rating": ["Dialogue Rating", None, 1],
            "acting_rating": ["Acting Rating", None, 1],
            "music_rating": ["Music Rating", None, 1]
        }
        # Automatically calculated based on categorical ratings
        self.total_rating = None
        # Overrides automatically calculated total rating if present
        self.total_rating_override = None
    
    def __str__(self):
        # Override calculated total rating if override rating is present
        total_rating = self.total_rating_override
        if total_rating is None:
            total_rating = self.total_rating
        # Total rating at the top
        rating_string = f"Total Rating: {total_rating}\n"
        # Add a line for each rating
        for category in self.ratings:
            rating_string += f"{self.ratings[category][0]}: {self.ratings[category][1]}\n"
        return rating_string
    
    def calculate_total_rating(self):
        average_rating = 0
        total_weight = 0
        # Sum weighted ratings and total weight
        for category_key in self.ratings:
            category = self.ratings[category_key]
            if category[1] is not None:
                average_rating += category[1] * category[2]
                total_weight += category[2]
        # Calculate total rating
        self.total_rating = average_rating / total_weight
    
    def update_rating(self, category, value, weight=None):
        # Update rating value
        self.ratings[category][1] = value
        # Update rating weight IF specified
        if weight is not None:
            self.ratings[category][2] = weight
        # Recalculate total rating with new values
        self.calculate_total_rating()

    def save(self, manager):
        # Save the current rating using the provided RatingManager.
        manager.add_or_update_rating(self)

    @classmethod
    def load(cls, content_id, manager):
        # Load a rating by content ID using the provided RatingManager.
        return manager.get_rating(content_id)
