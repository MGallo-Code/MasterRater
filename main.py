from APIManager import APIManager

class Rating:
    def __init__(self, content_id, content_type="movie", season_number=None, episode_number=None):
        # Represents show or movie ID
        self.content_id = content_id
        # Type of content, i.e. "movie" or "tv"
        self.content_type = content_type
        # Season number, if present
        self.season_number = season_number
        # Episode number, if present
        self.episode_number = episode_number
        # TODO: confirm content exists

        # Create default ratings,
        #(Rating Value, Weight)
        # (None, 1) is default, unrated
        self.ratings = {}
        self.ratings["plot_rating"] = ["Plot Rating", None, 1]
        self.ratings["aesthetic_rating"] = ["Aesthetic Rating", None, 1]
        self.ratings["immersion_rating"] = ["Immersion Rating", None, 1]
        self.ratings["charm_rating"] = ["Charm Rating", None, 1]
        self.ratings["humor_rating"] = ["Humor Rating", None, 1]
        self.ratings["horror_rating"] = ["Horror Rating", None, 1]
        self.ratings["dialogue_rating"] = ["Dialogue Rating", None, 1]
        self.ratings["acting_rating"] = ["Acting Rating", None, 1]
        self.ratings["music_rating"] = ["Music Rating", None, 1]
        
        self.total_rating = None

        # Override total rating if present
        self.total_rating_override = None
    
    def __str__(self):
        # Override calculated total rating if override rating is present
        total_rating = self.total_rating_override
        if total_rating is None:
            total_rating = self.total_rating
        # Total rating at the top
        rating_string = f"Total Rating:{total_rating}\n"
        # Add a line for each rating
        for category in self.ratings:
            rating_string += f"{self.ratings[category][0]}: {self.ratings[category][1]}\n"
        
        return rating_string
    
    def calculate_total_rating(self):
        average_rating = 0
        total_weight = 0
        for category_key in self.ratings:
            category = self.ratings[category_key]
            if category[1] is not None:
                # Multiply rating value by weight
                average_rating += category[1] * category[2]
                # Increment number of ratings based on weight
                total_weight += category[2]
        # Finish calculating total rating
        self.total_rating = average_rating / total_weight
    
    def update_rating(self, category, value, weight=None):
        # Update rating value
        self.ratings[category][1] = value
        # Update rating weight if specified
        if weight is not None:
            self.ratings[category][2] = weight
        # Update total rating with these new values
        self.calculate_total_rating()


# List of stored ratings
my_ratings = []

# Get user input from options, options MUST be lowercase
def get_input_from_options(prompt, options):
    user_input = ""
    while user_input not in options:
        # Get user input
        prompt += "(Enter " + ", ".join(options) + "):\n >> "
        user_input = input(prompt).lower()
    return user_input

# Search for show or movie
def search_for_content(api_manager):
    # Get user-selected content type
    content_type = get_input_from_options("Would you like to search for a movie or a TV show?", ["m", "tv"])
    # Set to api-accepted content-type based on user options
    if content_type.lower() == "m":
        content_type = "movie"
    elif content_type.lower() == "tv":
        content_type = "tv"

    # Get user input for search
    query = input(f"Search for {content_type}: ")
    # Search based on 
    results = m.get_search(query, content_type)

    # Get number of results
    num_results = len(results.json()['total_results'])
    print(f"{num_results} results found.")


    if num_results != 0:
        pass
    
    # If no results, return to top

    # Handle movie search results
    # Display results
    print("Results:")
    for i in range(len(results.json()['results'])):
        if content_type == "movie":
            print(f"{i+1}. {results.json()['results'][i]['title']}, {results.json()['results'][i]['release_date']}")
        elif content_type == "tv":
            print(f"{i+1}. {results.json()['results'][i]['name']}, {results.json()['results'][i]['first_air_date']}")

    # Get user input
    selection = int(input("Enter the number of the show or movie you would like to rate: "))
    selection = selection - 1
    selection_id = results.json()['results'][selection]['id']

    # Search for rating if it exists
    rating_exists = False
    for rating in my_ratings:
        print(f"Rating's ID: {rating.content_id}")
        if selection_id == rating.content_id:
            if content_type == "movie":
                print(f"Movie: {results.json()['results'][i]['title']}, {results.json()['results'][i]['release_date']}")
                print(rating)
            elif content_type == "tv":
                print(f"Show: {results.json()['results'][i]['name']}, {results.json()['results'][i]['first_air_date']}")
                print(rating)
            rating_exists = True
            break
    
    # If rating doesn't exist, ask user to create it
    if not rating_exists:
        # If content is tv show, ask to rate show or select season
        if content_type == "tv":

        # Ask user for new ratings
        rating = Rating(selection_id, content_type)
        for category_key in rating.ratings:
            category = rating.ratings[category_key]
            # Ask user for rating
            rating_value = input(f"{category[0]}: ")
            # If user doesn't enter a rating, skip this category
            if rating_value == '':
                continue
            else:
                rating_value = float(rating_value)
            # Ask user for weight
            weight = input(f"{category[0]} weight (1x, 2x, etc., format as '1', '1.1', etc.): ")
            # If user doesn't enter a weight, set it to 1
            if weight == '':
                weight = 1
            else:
                weight = float(weight)
            # Update rating
            rating.update_rating(category_key, rating_value, weight)
        my_ratings.append(rating)

        for rating in my_ratings:
            rating.calculate_total_rating()
            print(rating)



if __name__ == "__main__":
    m = APIManager()
    while True:
        search_for_content(m)



# m = APIManager()
# response = m.get_search("doctor who", "tv", 1)

# print(response.json()['results'][0]['id'])

# response = m.get_details(57243, "tv")
# number_of_seasons = response.json()["number_of_seasons"]

# response = m.get_season_details(57243, 6)
# print(response.json()["episodes"][0].keys())