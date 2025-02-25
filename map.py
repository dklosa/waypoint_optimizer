import streamlit as st
import pydeck as pdk

def map(df, route):
    route_data = [{"path": route}]
    layers = [
        pdk.Layer(
            "ScatterplotLayer",
            data=df,
            get_position="[lon, lat]",
            get_color="[200, 30, 0, 160]",
            get_radius=80,
        ),
        pdk.Layer(
            "PathLayer",
            data=route_data,
            get_path="path",
            get_color=[200, 30, 0, 160],
            width_scale=20,
            get_width=5,
            pickable=True,
        )
    ]

    deck = pdk.Deck(
        map_style=None,
        initial_view_state=pdk.ViewState(
            latitude=df.iloc[2:]["lat"].mean(),
            longitude=df.iloc[2:]["lon"].mean(),
            zoom=11,
            pitch=50,
        ),
        layers=layers
    )

    st.pydeck_chart(deck)