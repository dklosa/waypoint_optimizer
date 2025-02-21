import os
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
    if "routes" in data.keys():
        route_coordinates = data["routes"][0]["geometry"]["coordinates"]
        return route_coordinates
    return []

def travelingsalesman(start, target, waypoints=None):
    route_str = start_target_waypoints_to_str(start, target, waypoints)
    url = f"https://api.mapbox.com/optimized-trips/v1/mapbox/driving/{route_str}?geometries=geojson&source=first&destination=last&roundtrip=false&access_token={API_TOKEN}"
    response = requests.get(url)
    data = json.loads(response.text)
    if not data["code"] == "Ok":
        raise Exception("Something went wrong with Mapbox API when searching for optimal route.")
    if "trips" in data.keys():
        route_coordinates = data["trips"][0]["geometry"]["coordinates"]
        return route_coordinates
    return []

def start_target_waypoints_to_str(start, target, waypoints):
    route = f"{start[1]},{start[0]};"
    if isinstance(waypoints, list):
        for wp in waypoints:
            route += f"{wp[1]},{wp[0]};"
    route += f"{target[1]},{target[0]}"
    return route
