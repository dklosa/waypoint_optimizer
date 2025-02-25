from googlemaps import *
from map import map
from mapbox import *
import pandas as pd
import streamlit as st
from streamlit_searchbox import st_searchbox

st.set_page_config(
    page_title="Waypoint optimizer",
    page_icon=":car:",
)

if "clicks" not in st.session_state:
    st.session_state.clicks = {}

def click(key):
    st.session_state.clicks[key] = True

def unclick(key):
    st.session_state.clicks[key] = False

def isclicked(key):
    if not key in st.session_state.clicks.keys():
        return False
    return st.session_state.clicks[key]

if "checkpoints" not in st.session_state:
    st.session_state.checkpoints = []

def add_waypoint(waypoint):
    st.session_state.checkpoints.append(waypoint)

st.header("Waypoint optimizer :car:")

st.write("Select your starting address.")
start = st_searchbox(get_suggestions, "Start address", key="start")
st.write("Select your target address.")
target = st_searchbox(get_suggestions, "Target address", key="target")
st.write("Select your waypoint addresses (max 10).")
cp = st_searchbox(get_suggestions, "Waypoint address", key=f"waypoint_{len(st.session_state.checkpoints)}")
if st.button("Add waypoint after selecting.", key="add_waypoint") and len(st.session_state.checkpoints) < 10:
    add_waypoint(cp)

for i, address in enumerate(st.session_state.checkpoints):
    st.write(f"{i+1}. {address}")

if st.button("Submit addresses.", key="submit"):
    click("submit")

if isclicked("submit"):
    if not start or not target:
        st.exception(Exception("Start and Target need to be set."))
    start_coordinates = get_coordinates_from_address(start)
    target_coordinates = get_coordinates_from_address(target)
    checkpoints_coordinates = []
    parsed_checkpoints = []
    if st.session_state.checkpoints:
        for checkpoint in st.session_state.checkpoints:
            if checkpoint:
                checkpoints_coordinates.append(get_coordinates_from_address(checkpoint, prox=start_coordinates))
                parsed_checkpoints.append(checkpoint)
    df = pd.DataFrame([start_coordinates, target_coordinates, *checkpoints_coordinates],
                      columns=["lon", "lat"])
    route, checkpoint_order = travelingsalesman(start_coordinates[::-1], target_coordinates[::-1], [c[::-1] for c in checkpoints_coordinates])

    st.write("Best waypoint order:")
    for i, cp in enumerate([parsed_checkpoints[i] for i in checkpoint_order]):
        st.write(f"{i+1}. {cp}")
    st.write("Link to route on GoogleMaps:")
    st.write(create_google_maps_link([start] + [parsed_checkpoints[i] for i in checkpoint_order] + [target]))

    map(df, route)
