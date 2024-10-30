from Rating import Rating
from APIManager import APIManager

# Get user input from options, options MUST be lowercase
def get_input_from_options(prompt, options):
    user_input = None
    while user_input not in options:
        # Get user input
        user_input = input(prompt + "\n>> ").lower()
    return user_input

# Search for show or movie
def search_for_content(api_manager):
    # Get user-selected content type
    content_type = get_input_from_options("Would you like to search for a movie or a TV show? (Enter m or tv)", ["m", "tv"])
    # Set to api-accepted content-type based on user options
    if content_type.lower() == "m":
        content_type = "movie"
    elif content_type.lower() == "tv":
        content_type = "tv"

    # Get user input for search
    query = input(f"Search for {content_type}: ")
    # Search based on content type
    results = m.get_search(query, content_type)

    # Get number of results
    num_results = len(results)
    print(f"{num_results} results found.")

    # If results, display them
    if num_results != 0 and content_type == "movie":
        display_movie_results(results)
    if num_results != 0 and content_type == "tv":    
        display_tv_results(api_manager, results)
    # If no results, do nothing

def display_movie_results(results):
    global my_movie_ratings

    # Handle movie search results
    # Display results
    print("Results:")
    for i, option in enumerate(results):
        print(f"{i+1}. {option['title']}, {option['release_date']}")

    # Get user input
    selection = int(input("Enter the number of the show or movie you would like to rate:\n>> "))
    selected_movie = results[selection - 1]

    # Display information for selected show or movie
    print(f"Selected Movie:\n" +
        f" {selected_movie['title']}, {selected_movie['release_date']}\n" +
        f"  Overview: {selected_movie['overview']}\n" +
        f"  Global Rating: {selected_movie['vote_average']}\n")
    # Search for rating if it exists
    rating_exists = False
    # Check if rating with selection's id exists
    movie_id = selected_movie['id']
    if movie_id in my_movie_ratings:
        rating_exists = True
        rating = my_movie_ratings[movie_id]
        print("Your Ratings:")
        print(rating)
    
    # Ask user if they want to rate/rerate the movie or return to search
    if not rating_exists:
        user_choice = get_input_from_options("What would you like to do?\n" +
                                             "  1. Rate this movie\n" +
                                             "  2. Select another movie or tv show", ['1', '2'])
    else:
        user_choice = get_input_from_options("What would you like to do?\n" +
                                             "  1. Rate this movie again\n" +
                                             "  2. Select another movie or tv show", ['1', '2'])

    # User wants to rate the movie.
    if user_choice == '1':
        # Load rating if it exists
        rating = None
        if rating_exists:
            rating = my_movie_ratings[movie_id]
        else:
            rating = Rating(movie_id, 'movie')
        # Ask user for new ratings
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
        my_movie_ratings[movie_id] = rating
        print("<><><><> Your rating has been saved! <><><><>")
        print(rating)
    # Otherwise, return to search

def display_tv_results(api_manager, results):
    global my_tv_ratings

    # Display tv search results
    print("Results:")
    for i, option in enumerate(results):
        print(f"{i+1}. {option['name']}, {option['first_air_date']}")

    # Get user input
    selection = int(input("Enter the number of the show or movie you would like to rate:\n>> "))
    selected_show = results[selection - 1]

    # Display information for selected show
    display_show_details(api_manager, str(selected_show['id']))

def display_show_details(api_manager, show_id):
    # Get details for selected show
    selected_show = m.get_details(show_id, 'tv')
    # Display information for selected show or movie
    print(f"Selected TV Show:\n" +
        f" {selected_show['name']}, {selected_show['first_air_date']}\n" +
        f"  {selected_show['number_of_seasons']} Seasons\n" +
        f"  Overview: {selected_show['overview']}\n" +
        f"  Global Rating: {selected_show['vote_average']}\n")
    # Search for rating if it exists
    rating_exists = False
    # Check if rating with selection's id exists
    if show_id in my_tv_ratings:
        rating_exists = True
        rating = my_tv_ratings[show_id]
        print("Your Ratings:")
        print(rating)
    
    # Ask user if they want to rate/rerate the movie or return to search
    if not rating_exists:
        user_choice = get_input_from_options("What would you like to do?\n" +
                                             "  1. Rate this tv show\n" +
                                             "  2. Select a season of this show to review\n" +
                                             "  3. Select another movie or tv show", ['1', '2', '3'])
    else:
        user_choice = get_input_from_options("What would you like to do?\n" +
                                             "  1. Rate this tv show again\n" +
                                             "  2. Select a season of this show to review\n" +
                                             "  3. Select another movie or tv show", ['1', '2', '3'])

    # User wants to rate or re-rate the tv show.
    if user_choice == '1':
        # Load previous rating if it exists
        rating = None
        if rating_exists:
            rating = my_tv_ratings[show_id]
        else:
            rating = Rating(show_id, 'tv')
        # Ask user for new ratings
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
        my_tv_ratings[show_id] = rating
        print("<><><><> Your rating has been saved! <><><><>")
        # Return to show_details screen to display new rating
        display_show_details(api_manager, show_id)
    # User wants to select a season
    elif user_choice == '2':
        display_season_details(api_manager, selected_show)
    # Otherwise, return to search

def display_season_details(api_manager, show):
    global my_tv_ratings

    # Display season selection options
    # Create list with possible user inputs (season numbers, or '' to return to search)
    season_options = [str(i) for i in range(1, show['number_of_seasons'] + 1)]
    season_options.append('')
    # Get user choice
    user_choice = get_input_from_options("Please select a season to review (1 - " + str(show['number_of_seasons']) + "),\n" +
                                         " OR press Enter/Return to select another movie or tv show", season_options)

    # Return to menu if season number is not provided
    if user_choice == '':
        return
    # Only remaining options are integers representing season numbers...
    selected_season = int(user_choice)

    # Otherwise, get season information
    season_details = api_manager.get_season_details(str(show['id']), selected_season)
    # Display information for season
    # Display information for season
    print(f"Selected Season:\n" +
        f" Season {season_details['season_number']}\n" +
        f" Air Date: {season_details['air_date']}\n" +
        f" Overview: {season_details['overview']}\n" +
        f" Global Rating: {season_details['vote_average']}\n")

    # Search for rating if it exists
    rating_exists = False
    # Check if rating with selection's id exists
    rating_id = str(show['id']) + "-S" + str(selected_season)
    if rating_id in my_tv_ratings:
        rating_exists = True
        rating = my_tv_ratings[rating_id]
        print("Your Ratings:")
        print(rating)
    
    # Ask user if they want to rate/rerate the movie or return to search
    user_choice = None
    if not rating_exists:
        user_choice = get_input_from_options("What would you like to do?\n" +
                                             "  1. Rate this season\n" +
                                             "  2. Select an episode of this show to review\n" +
                                             "  3. Select another season to review\n" +
                                             "  4. Select another movie or tv show", ['1', '2', '3', '4'])
    else:
        user_choice = get_input_from_options("What would you like to do?\n" +
                                             "  1. Rate this season again\n" +
                                             "  2. Select an episode of this show to review\n" +
                                             "  3. Select another season to review\n" +
                                             "  4. Select another movie or tv show", ['1', '2', '3', '4'])

    # User wants to rate or re-rate the tv show.
    if user_choice == '1':
        # Load previous rating if it exists
        rating = None
        if rating_exists:
            rating = my_movie_ratings[rating_id]
        else:
            rating = Rating(rating_id, 'tv')
        # Ask user for new ratings
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
        my_tv_ratings[rating_id] = rating
        print("<><><><> Your rating has been saved! <><><><>")
        # Return to season_details menu to show rating
        display_season_details(api_manager, show)
    # User wants to select an episode
    elif user_choice == '2':
        display_episode_details(api_manager, show, selected_season)
    # User wants to select another season
    elif user_choice == '3':
        display_season_details(api_manager, show)
    # Otherwise, return to search

def display_episode_details(api_manager, show, season_number):
    global my_tv_ratings
    
    # Get season details including episodes
    season_details = api_manager.get_season_details(str(show['id']), season_number)
    
    # Display episode selection options
    print(f"Season {season_number} Episodes:")
    for episode in season_details['episodes']:
        print(f"{episode['episode_number']}. {episode['name']} (Air Date: {episode['air_date']})")
    
    # Get user input for episode selection
    episode_number = int(input(f"Select an episode to review (1 - {len(season_details['episodes'])}):\n>> "))
    
    # Validate episode number
    selected_episode = None
    for episode in season_details['episodes']:
        if episode['episode_number'] == episode_number:
            selected_episode = episode
            break
    
    if not selected_episode:
        print("Invalid episode selection. Please try again.")
        return
    
    # Display selected episode details
    print(f"Selected Episode:\n" +
          f" {selected_episode['name']}, {selected_episode['air_date']}\n" +
          f" Overview: {selected_episode['overview']}\n" +
          f" Global Rating: {selected_episode['vote_average']}\n")
    
    # Check if a rating for this episode already exists
    episode_id = str(show['id']) + "-S" + str(season_number) + "-E" + str(episode_number)
    rating_exists = False
    if episode_id in my_tv_ratings:
        rating_exists = True
        rating = my_tv_ratings[episode_id]
        print("Your Ratings:")
        print(rating)
    
    # Ask user if they want to rate/rerate the episode or return to search
    if not rating_exists:
        user_choice = get_input_from_options("What would you like to do?\n" +
                                             "  1. Rate this episode\n" +
                                             "  2. Select another episode to review\n" +
                                             "  3. Select another season to review\n" +
                                             "  4. Select another movie or tv show", ['1', '2', '3', '4'])
    else:
        user_choice = get_input_from_options("What would you like to do?\n" +
                                             "  1. Rate this episode again\n" +
                                             "  2. Select another episode to review\n" +
                                             "  3. Select another season to review\n" +
                                             "  4. Select another movie or tv show", ['1', '2', '3', '4'])

    # User wants to rate or re-rate the episode.
    if user_choice == '1':
        # Load previous rating if it exists
        rating = None
        if rating_exists:
            rating = my_tv_ratings[episode_id]
        else:
            rating = Rating(episode_id, 'tv', season_number, episode_number)
        
        # Ask user for new ratings
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
        
        my_tv_ratings[episode_id] = rating
        print("<><><><> Your rating has been saved! <><><><>")
        # Return to show_details screen to display new rating
        display_episode_details(api_manager, show, season_number)
    
    # User wants to select another episode
    elif user_choice == '2':
        display_episode_details(api_manager, show, season_number)
    
    # User wants to select another season
    elif user_choice == '3':
        display_season_details(api_manager, show)
    
    # Otherwise, return to search

# List of stored ratings
my_movie_ratings = {}
my_tv_ratings = {}

if __name__ == "__main__":
    m = APIManager()
    while True:
        search_for_content(m)