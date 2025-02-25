from googlemaps import *
from map import map
from mapbox import *
import pandas as pd
import streamlit as st

st.session_state.clicks = {}

def click(key):
    st.session_state.clicks[key] = True

def unclick(key):
    st.session_state.clicks[key] = False

def isclicked(key):
    if not key in st.session_state.clicks.keys():
        return False
    return st.session_state.clicks[key]

start = st.text_input("Start address.", key="start")
target = st.text_input("Target address.", key="target")
checkpoints = st.text_area("Waypoint addresses.", key="waypoints")

if st.button("Submit addresses.", key="submit"):
    click("submit")

if isclicked("submit"):
    if not start or not target:
        st.exception(Exception("Start and Target need to be set."))
    start_coordinates = get_coordinates_from_address(start, country)
    target_coordinates = get_coordinates_from_address(target, country)
    checkpoints_coordinates = []
    parsed_checkpoints = []
    if checkpoints:
        for checkpoint in checkpoints.split("\n"):
            if checkpoint:
                checkpoints_coordinates.append(get_coordinates_from_address(checkpoint, country))
                parsed_checkpoints.append(checkpoint)
    df = pd.DataFrame([start_coordinates, target_coordinates, *checkpoints_coordinates],
                      columns=["lon", "lat"])
    route, checkpoint_order = travelingsalesman(start_coordinates[::-1], target_coordinates[::-1], [c[::-1] for c in checkpoints_coordinates])
    map(df, route)
    st.write("Link to route on GoogleMaps:")
    st.write(create_google_maps_link([start] + [parsed_checkpoints[i] for i in checkpoint_order] + [target]))
