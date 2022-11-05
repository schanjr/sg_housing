import streamlit as st
import pandas as pd
import pydeck as pdk
import altair as alt
import lib.calculations as calc

df = pd.read_csv('./resale-flat-prices/2017-and-beyond-annotated.csv')


@st.cache
def flat_types():
    return df.flat_type.unique()


@st.cache
def towns():
    return df.town.unique()


with st.sidebar:
    with st.form(key='Housing Data Filters'):
        selected_flat_types = st.multiselect("Flat Types", flat_types(), flat_types()[:3])
        df = df[df.flat_type.isin(selected_flat_types)]
        selected_town = st.multiselect('Town', towns(), towns(), label_visibility="hidden")
        df = df[df.town.isin(selected_town)]
        df['sqr_ft'] = df['floor_area_sqm'].apply(calc.sqm_to_sqft)
        st.form_submit_button("Submit")

df['month'] = pd.to_datetime(df['month'])
df = df[df["month"] > "2018-01-01"]
st.write("Rows: {}".format(df.size))

st.write(df.sample(n=5))

# chart = alt.Chart(df) \
#     .mark_point() \
#     .encode(x='month', y='resale_price', color='flat_type') \
#     .properties(width=1000, height=800)
# st.altair_chart(chart)


# Define a layer to display on a map
layer = pdk.Layer(
    "HexagonLayer",
    data=df,
    get_position=["longitude", "latitude"],
    auto_highlight=True,
    elevation_scale=75,
    pickable=True,
    elevation_range=[0, 100],
    extruded=True,
    coverage=1,
    radius=50
)

# Set the viewport location
view_state = pdk.ViewState(
    longitude=df.iloc[0]['longitude'],
    latitude=df.iloc[0]['latitude'],
    zoom=10,
    min_zoom=5,
    max_zoom=15,
    pitch=40.5,
    bearing=-27.36,
)

# Render
deck = pdk.Deck(
    map_provider='mapbox',
    map_style='mapbox://styles/schanjr/cla4gffe3001l14o4ql60p13j',
    layers=[layer], initial_view_state=view_state)
st.components.v1.html(deck.to_html(as_string=True), height=600)
# st.pydeck_chart(deck)
