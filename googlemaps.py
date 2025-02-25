import urllib.parse

def create_google_maps_link(waypoints):
    base_url = "https://www.google.com/maps/dir/"
    encoded_waypoints = "/".join(urllib.parse.quote(waypoint) for waypoint in waypoints)
    return base_url + encoded_waypoints