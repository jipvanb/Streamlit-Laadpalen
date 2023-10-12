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

for i in openchargemap.index:
    row = openchargemap.loc[i]
    location = [row['Latitude'], row['Longitude']]
    popup = f'Number of Points: {row["NumberOfPoints"]}<br><br>Connection Type: {row["ConnectionTypeID"]}<br><br>Level: {row["LevelID"]}<br><br>Amps: {row["Amps"]}<br><br>Voltage: {row["Voltage"]}<br><br>Power(kw): {row["PowerKW"]}<br><br>Current Type: {row["CurrentTypeID"]}<br><br>Quantity: {row["Quantity"]}'
    color = color_producer(row['LevelID'])
    fill_color = color

    folium.Circle(
        location=location,
        popup=popup,
        color=color,
        fill=True,
        fill_color=fill_color,
        radius=150,
        weight=1,
        opacity=0.5,
        fillOpacity=0.1
    ).add_to(m)

st_map = folium_static(m, width=1200, height=700)
try: 
    st_map
except:
    print('error')