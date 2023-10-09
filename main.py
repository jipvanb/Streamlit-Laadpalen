import streamlit as st

import requests
import pandas as pd
import numpy as np
import plotly.express as px
import matplotlib.pyplot as plt

st.set_page_config(
    page_title='Elektrische mobiliteit & laadpalen',
    layout='wide'
)

# load data
laadpaaldata = pd.read_csv('laadpaaldata.csv')
# voertuigen = pd.read_csv('elektrischeVoertuigen.csv')
key = "b2451f45-7af1-4a46-a430-8496d6583401"
res = requests.get(
    f"https://api.openchargemap.io/v3/poi/?output=json&countrycode=NL&maxresults=10000&compact=true&verbose=false&key={key}")
data = res.json()
openchargemap = pd.json_normalize(data)
df4 = pd.json_normalize(openchargemap.Connections)
df5 = pd.json_normalize(df4[0])
openchargemap = pd.concat([openchargemap, df5], axis=1)
openchargemap.drop(columns=['Connections'], inplace=True)
# TODO clean data
laadpaaldata['Started'] = pd.to_datetime(laadpaaldata['Started'], format='%Y-%m-%d %H:%M:%S', errors='coerce')
laadpaaldata['Ended'] = pd.to_datetime(laadpaaldata['Ended'], format='%Y-%m-%d %H:%M:%S', errors='coerce')
laadpaaldata.dropna(subset=['Started'], inplace=True)
laadpaaldata.dropna(subset=['Ended'], inplace=True)

# Drop rows with negative charging times
rows_to_drop = laadpaaldata[((laadpaaldata['ChargeTime']) < 0)].index
laadpaaldata.drop(index=rows_to_drop, inplace=True)

# Convert power in Watt to kiloWatt
laadpaaldata['TotalEnergy'] = round((laadpaaldata['TotalEnergy'] / 1000), 2)
laadpaaldata['MaxPower'] = round(laadpaaldata['MaxPower'] / 1000, 2)
# Efficiency calculation
laadpaaldata['Efficiency'] = (round((laadpaaldata['ChargeTime'] / laadpaaldata['ConnectedTime']) * 100, 2))

print(laadpaaldata.agg({'Efficiency': ['max', 'min', 'mean']}))


# TODO drop unnecessary columns

# TODO merge data

# Streamlit dashboard code
st.title('Elektrische mobiliteit & laadpalen')

# Container 1: Metrics
metric1, metric2, metric3, metric4 = st.columns(4)
# Get average charging time
charge_time = (laadpaaldata['ChargeTime'].mean()) * 60
connected_time = laadpaaldata['ConnectedTime'].mean() * 60
# Convert to hours and minutes
hours_charge, minutes_charge = divmod(charge_time, 60)
hours_conn, minutes_conn = divmod(connected_time, 60)


consumption = laadpaaldata['MaxPower'].mean()
avg_eff = laadpaaldata['Efficiency'].mean()
metric1.metric(
    label='Gem. Laadtijd',
    value=f" {int(hours_charge)} uur {int(minutes_charge)} min"
)
metric2.metric(
    label='Gem. Tijd aan de laadpaal',
    value=f" {int(hours_conn)} uur {int(minutes_conn)} min"
)
metric3.metric(
    label='Gem. Efficientie',
    value=f"{round(avg_eff, 2)} %"
)
metric4.metric(
    label='Gem. Verbruik (kWh)',
    value=f" {round(consumption, 2)} kWh"
)
# Container 2: Charts
fig_col1, fig_col2 = st.columns(2)
df_grouped_day = laadpaaldata.groupby(pd.Grouper(key='Started', freq='D')).sum()
with fig_col1:
    st.markdown('### First Chart')
    st.line_chart(df_grouped_day, y='TotalEnergy')
with fig_col2:
    st.markdown('### Second Chart')
    st.bar_chart(df_grouped_day, y='MaxPower')

st.bar_chart(laadpaaldata, x='TotalEnergy', y='Efficiency')