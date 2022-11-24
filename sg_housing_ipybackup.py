import pandas as pd
import altair as alt

df = pd.read_csv('sg_housing/resale-flat-prices/2017-and-beyond-annotated.csv')
# # Cell for getting coordinates, don't need to run this usually.
# import pandas as pd
# import lib.map_utils as mp
# import importlib
# importlib.reload(mp)
#
#
#
# # df = pd.read_csv('./resale-flat-prices/resale-flat-prices-based-on-registration-date-from-jan-2017-onwards.csv')
# map_urls = list(map(mp.map_search_url, df.street_name.unique()))
# results = mp.parallelize_http(map_urls)
# map_url_memo = {}
# for res in results:
#     search_val = res['response_obj'].url_obj.query['searchVal']
#     map_url_memo[search_val] = res['body']['results'][0]
#
# for index, row in df.iterrows():
#     map_data = map_url_memo[row.street_name]
#     df.at[index, 'longitude'] =  map_data['LONGITUDE']
#     df.at[index, 'latitude'] =  map_data['LATITUDE']
#     df.at[index, 'postal'] = map_data['POSTAL']
# df.to_csv('./resale-flat-prices/2017-and-beyond-annotated.csv')



df['month'] = pd.to_datetime(df['month'])
df = df[df["month"] >"2018-01-01"]
df

alt.data_transformers.enable('default', max_rows=None)
alt.Chart(df).mark_line().encode(x='month',y='resale_price',color='flat_type', strokeDash='flat_type',)



import pydeck as pdk

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
    radius=200
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
r = pdk.Deck(layers=[layer], initial_view_state=view_state)
r.to_html("hexagon_layer.html")
