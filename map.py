import streamlit as st
import pydeck as pdk

def map(df):
    st.pydeck_chart(
        pdk.Deck(
            map_style=None,
            initial_view_state=pdk.ViewState(
                latitude=df["lat"].mean(),
                longitude=df["lon"].mean(),
                zoom=14,
                pitch=50,
            ),
            layers=[
                pdk.Layer(
                    "ScatterplotLayer",
                    data=df,
                    get_position="[lon, lat]",
                    get_color="[200, 30, 0, 160]",
                    get_radius=30,
                ),
            ],
        )
    )