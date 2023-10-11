from main import openchargemap
import folium
import streamlit as st
from streamlit_folium import st_folium, folium_static
import matplotlib.colors as mcolors

# Folium map
def color_producer(type):
    if type == 1:
        return mcolors.CSS4_COLORS['green']
    if type == 2:
        return mcolors.CSS4_COLORS['orange']
    if type == 3:
        return mcolors.CSS4_COLORS['red']
    return 'gray'

m = folium.Map(location=[52.0893191, 5.1101691], zoom_start=8, tiles='cartodbpositron')

max_radius = 850
min_radius = 700
max_value = openchargemap['NumberOfPoints'].max()
min_value = openchargemap['NumberOfPoints'].min()

for i in openchargemap.index:
    row = openchargemap.loc[i]
    location = [row['Latitude'], row['Longitude']]
    popup = f'Number of Points: {row["NumberOfPoints"]}<br>Connection Type: {row["ConnectionTypeID"]}<br>Level: {row["LevelID"]}<br>Amps: {row["Amps"]}<br>Voltage: {row["Voltage"]}<br>Power(kw): {row["PowerKW"]}<br>Current Type: {row["CurrentTypeID"]}<br>Quantity: {row["Quantity"]}'
    # tooltip = row['Gebruiksdoel']
    color = color_producer(row['LevelID'])
    fill_color = color
    scaled_value = (row['NumberOfPoints'] - min_value) / (max_value - min_value)
    radius = min_radius + (max_radius - min_radius) * scaled_value
    
    folium.Circle(
        location=location,
        popup=popup,
        # tooltip=tooltip,
        color=color,
        fill=True,
        fill_color=fill_color,
        radius=radius,
        weight=1,
        opacity=0.5,
        fillOpacity=0.1
    ).add_to(m)
st_map = folium_static(m, width=1200, height=700)
st_map