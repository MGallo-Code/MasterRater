from dotenv import load_dotenv
import os
import requests

# Load env variables from .env
load_dotenv()
bearer_token = os.getenv("BEARER_TOKEN")

url = "https://api.themoviedb.org/3/configuration"
headers = {
    "accept": "application/json",
    "Authorization": "Bearer " + bearer_token
}