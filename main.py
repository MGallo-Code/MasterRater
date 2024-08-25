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

# Get user input from options, options MUST be lowercase
def get_input_from_options(prompt, options):
    while user_input not in options:
        # Get user input
        user_input = input(prompt + "\n>> ").lower()
    return user_input

# Search for show or movie
def search_for_content(api_manager):
    # Get user-selected content type
    content_type = get_input_from_options("Would you like to search for a movie or a TV show (Enter m or tv)?", ["m", "tv"])
    # Set to api-accepted content-type based on user options
    if content_type.lower() == "m":
        content_type = "movie"
    elif content_type.lower() == "tv":
        content_type = "tv"

    # Get user input for search
    query = input(f"Search for {content_type}: ")
    # Search based on content type
    results = m.get_search(query, content_type)
    results = results.json()["results"]

    # Get number of results
    num_results = len(results)
    print(f"{num_results} results found.")

    # If results, display them
    if num_results != 0 and content_type == "movie":
        display_movie_results(api_manager, content_type, results)
    if num_results != 0 and content_type == "tv":    
        display_tv_results(api_manager, content_type, results)
    # If no results, do nothing

def display_movie_results(api_manager, content_type, results):
    global my_movie_ratings

    # Handle movie search results
    # Display results
    print("Results:")
    for i, option in enumerate(results):
        if content_type == "movie":
            print(f"{i+1}. {option['title']}, {option['release_date']}")
        elif content_type == "tv":
            print(f"{i+1}. {option['name']}, {option['first_air_date']}")

    # Get user input
    selection = int(input("Enter the number of the show or movie you would like to rate: "))
    selected_movie = results[selection - 1]

    # Display information for selected show or movie
    print(f"Selected Movie:\n\
          \tName: {selected_movie['title']}, {selected_movie['release_date']}\n\
          \tOverview: {selected_movie['overview']}\n\
          \tGlobal Rating: {selected_movie['vote_average']}\n")
    # Search for rating if it exists
    rating_exists = False
    for rating_id in my_movie_ratings:
        if selected_movie['id'] == my_movie_ratings[rating_id].content_id and content_type == "movie":
            print("Your Ratings:")
            print(rating)
            rating_exists = True
            break
    
    # Ask user if they want to rate/rerate the movie or return to search
    if not rating_exists:
        user_choice = get_input_from_options("What would you like to do?\n\
                            \t1. Rate this movie\n\
                            \t2. Select another movie", ['1', '2'])
    else:
        user_choice = get_input_from_options("What would you like to do?\n\
                            \t1. Rate this movie again\n\
                            \t2. Select another movie", ['1', '2'])
        # If user wants to rerate, clear previous rating


    # User wants to rate the movie.
    if user_choice == '1':
        # Ask user for new ratings
        rating = Rating(selected_movie['id'], content_type)
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

def display_tv_results(api_manager, content_type, results):
    if content_type == "tv":
        print(f"Show: {results.json()['results'][1]['name']}, {results.json()['results'][i]['first_air_date']}")
        rating = Rating(1, "tv")
        print(rating)

# List of stored ratings
my_movie_ratings = []

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