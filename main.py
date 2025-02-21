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
