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
voertuigen = pd.read_csv('elektrischeVoertuigen.csv')
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

# TODO drop unnecessary columns

# TODO merge data

# Streamlit dashboard code
st.title('Elektrische mobiliteit & laadpalen')
print(laadpaaldata.mean())
# Container 1: Metrics
metric1, metric2, metric3 = st.columns(3)
charge_time = laadpaaldata['ChargeTime'].mean()
connected_time = laadpaaldata['ConnectedTime'].mean()
consumption = laadpaaldata['MaxPower'].mean()
metric1.metric(
    label='Avg. charge time',
    value=f" {round(charge_time, 2)} uur"
)
metric2.metric(
    label='Avg. connected Time',
    value=f" {round(connected_time, 2)} uur"
)
metric3.metric(
    label='Avg. Consumption (kWh)',
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

st.scatter_chart(df_grouped_day)