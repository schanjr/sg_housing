import pandas as pd
import pydeck as pdk
import streamlit as st
from tools import calculations as calc

import os
import sys

current_path = os.getcwd()
sys.path.append(os.path.join(current_path, "tools"))
print(sys.path)

st.set_page_config(layout="wide")

df = pd.read_csv('resale-flat-prices/2017-and-beyond-annotated.csv')
df['month'] = pd.to_datetime(df.month)


@st.cache
def flat_types():
    return df.flat_type.unique()


@st.cache
def towns():
    return df.town.unique()


with st.sidebar:
    st.title('Map Filters')
    with st.form(key='Housing Data Filters'):
        st.form_submit_button("Submit")
        # Flat Type filters
        selected_flat_types = st.multiselect("Flat Types", flat_types(), flat_types())
        df = df[df.flat_type.isin(selected_flat_types)]
        # Resale filters
        resale_min, resale_max = int(df.resale_price.min()), int(df.resale_price.max())
        resale_slider_min, resale_slider_max = st.slider('Resale Price ', min_value=resale_min, max_value=resale_max,
                                                         value=(resale_min, resale_max), format="SGD %d",
                                                         key='resale_price_slider', step=10000)
        df = df[df['resale_price'].between(resale_slider_min, resale_slider_max)]
        # Sqr feet filters
        df['sqr_ft'] = df['floor_area_sqm'].apply(calc.sqm_to_sqft)
        sqr_ft_min, sqr_ft_max = int(df.sqr_ft.min()), int(df.sqr_ft.max())
        sqr_ft_slider_min, sqr_ft_slider_max = st.slider('Square Feet', min_value=sqr_ft_min, max_value=sqr_ft_max,
                                                         value=(sqr_ft_min, sqr_ft_max), format="%d sqr/ft",
                                                         key='sqr_ft_slider')
        df = df[df['sqr_ft'].between(sqr_ft_slider_min, sqr_ft_slider_max)]
        # Month Sold filteres
        month_min, month_max = df.month.min(), df.month.max()
        start_date = st.date_input('Start date', month_min)
        end_date = st.date_input('End date', month_max)
        df = df[df['month'].between(pd.to_datetime(start_date), pd.to_datetime(end_date))]
        # Towns filters
        selected_town = st.multiselect('Town', towns(), towns())
        df = df[df.town.isin(selected_town)]
st.write("Rows: {}".format(df.size))

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
st.components.v1.html(deck.to_html(as_string=True), height=1000)  # , height=1000, width=1200)
# st.pydeck_chart(deck)

st.write(df.sample(n=20, replace=True))

if __name__ == "__main__":
    import sys
    sys.path.insert(0, '..')
