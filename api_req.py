import requests

url = "https://api.themoviedb.org/3/configuration"

headers = {
    "accept": "application/json",
    "Authorization": "Bearer " + bearer_token
}