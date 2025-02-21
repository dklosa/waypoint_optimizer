import streamlit as st

start = st.text_input("Start address.", key="start")
target = st.text_input("Target address.", key="target")
checkpoints = st.text_area("Waypoint addresses.", key="waypoints")

