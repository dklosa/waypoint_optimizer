import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()
API_TOKEN = os.getenv("MAPBOX_API_TOKEN")

def get_coordinates_from_address(address):
    url = f"https://api.mapbox.com/search/geocode/v6/forward?q={address}&access_token={API_TOKEN}"
    response = requests.get(url)
    data = json.loads(response.text)
    return data
