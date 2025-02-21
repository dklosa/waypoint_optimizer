import os
import pandas as pd
import requests
import json
from dotenv import load_dotenv

load_dotenv()
API_TOKEN = os.getenv("MAPBOX_API_TOKEN")

class CoordinatesNotFoundException(Exception):
    def __init__(self, address):
        self.message = f"Coordinates were not found for address {address}"
        super().__init__(self.message)

def get_coordinates_from_address(address):
    url = f"https://api.mapbox.com/search/geocode/v6/forward?q={address}&limit=1&access_token={API_TOKEN}"
    response = requests.get(url)
    data = json.loads(response.text)
    if len(data["features"]) == 0:
        raise CoordinatesNotFoundException(address)
    feature = data["features"][0]
    if not "geometry" in feature.keys():
        raise Exception("Something went wrong when calling Mapbox API.")
    coordinates = feature["geometry"]["coordinates"]
    return coordinates

def get_route(start, target, waypoints=None):
    route_str = start_target_waypoints_to_str(start, target, waypoints)
    url = f"https://api.mapbox.com/directions/v5/mapbox/driving/{route_str}?geometries=geojson&access_token={API_TOKEN}"
    response = requests.get(url)
    data = json.loads(response.text)
    if "routes" in data:
        route_coordinates = data["routes"][0]["geometry"]["coordinates"]
        return pd.DataFrame(route_coordinates,
                      columns=["lon", "lat"])
    return []
    response = requests.get(url)
    data = json.loads(response.text)
    return data
