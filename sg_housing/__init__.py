import streamlit as st
import pandas as pd
import altair as alt

df = pd.read_csv('./resale-flat-prices/resale-flat-prices-based-on-registration-date-from-jan-2017-onwards.csv')
flat_types = df.flat_type.unique()
selected_flat_types = st.multiselect("Flat Types", flat_types, flat_types[:3])

df['month'] = pd.to_datetime(df['month'])
df = df[df["month"] > "2018-01-01"]
df = df[df.flat_type.isin(selected_flat_types)]
df['price/sqm'] = df['resale_price'] / df['floor_area_sqm']

st.write(df)

chart = alt.Chart(df)\
            .mark_point()\
            .encode(x='month', y='resale_price', color='flat_type')\
            .properties(width=1000, height=800) \


st.altair_chart(chart)
#%%
