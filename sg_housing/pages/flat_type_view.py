import streamlit as st

st.write('Reference: https://www.mynicehome.gov.sg/')
two_rm_blush, two_rm_modern, three_rm_retro, four_rm_nordic, five_rm_luxe = st.tabs(["2 Room Flexi Blush", "2 Room Flexi Modern", "3 Room Retro", "4 Room Nordic", "5 Room Luxe"])


with two_rm_blush:
    st.header("2 Room Flexi (36m2) Blush")
    st.components.v1.html(f'<iframe height=1000 width=1000 '
                          f'src="https://assets.hdb.gov.sg/residential/buying-a-flat/finding-a-flat/my-nice-home-gallery/eamnh/2room36.html">'
                          f'</iframe>',
                          height=1000,
                          width=1000)

with two_rm_modern:
    st.header("2 Room Flexi (46m2) Mid Century Modern")
    st.components.v1.html(f'<iframe height=1000 width=1000 '
                          f'src="https://assets.hdb.gov.sg/residential/buying-a-flat/finding-a-flat/my-nice-home-gallery/eamnh/2room46.html">'
                          f'</iframe>',
                          height=1000,
                          width=1000)

with three_rm_retro:
    st.header("3 Room Retro (66m2) Retro Fun")
    st.components.v1.html(f'<iframe height=1000 width=1000 '
                          f'src="https://assets.hdb.gov.sg/residential/buying-a-flat/finding-a-flat/my-nice-home-gallery/eamnh/3room.html">'
                          f'</iframe>',
                          height=1000,
                          width=1000)

with four_rm_nordic:
    st.header("4 Room Nordic (90m2) Nordic Silhouette")
    st.components.v1.html(f'<iframe height=1000 width=1000 '
                          f'src="https://assets.hdb.gov.sg/residential/buying-a-flat/finding-a-flat/my-nice-home-gallery/eamnh/4room.html">'
                          f'</iframe>',
                          height=1000,
                          width=1000)

with five_rm_luxe:
    st.header("5 Room Nordic (110m2) Tropical Luxe")
    st.components.v1.html(f'<iframe height=1000 width=1000 '
                          f'src="https://assets.hdb.gov.sg/residential/buying-a-flat/finding-a-flat/my-nice-home-gallery/eamnh/5room.html">'
                          f'</iframe>',
                          height=1000,
                          width=1000)

