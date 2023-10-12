import time
import math
import streamlit as st
import requests
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt

st.set_page_config(
    page_title='Elektrische mobiliteit & laadpalen',
    layout='wide'
)
# Initialization of session state variables
if 'efficiency' not in st.session_state:
    st.session_state['efficiency'] = 0
if 'consumption' not in st.session_state:
    st.session_state['consumption'] = 0
if 'charge_hours' not in st.session_state:
    st.session_state['charge_hours'] = 0
if 'charge_minutes' not in st.session_state:
    st.session_state['charge_minutes'] = 0
if 'conn_hours' not in st.session_state:
    st.session_state['conn_hours'] = 0
if 'conn_minutes' not in st.session_state:
    st.session_state['conn_minutes'] = 0



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
chargemapcolumns = ['NumberOfPoints', 'AddressInfo.Latitude', 'AddressInfo.Longitude', 'ConnectionTypeID', 'LevelID', 'Amps', 'Voltage', 'PowerKW', 'CurrentTypeID', 'Quantity']
openchargemap = openchargemap[chargemapcolumns]
openchargemap.rename(columns={'AddressInfo.Latitude': 'Latitude', 'AddressInfo.Longitude': 'Longitude'}, inplace=True)

# Drop rows with negative charging times
rows_to_drop = laadpaaldata[((laadpaaldata['ChargeTime']) <= 0.166)].index
laadpaaldata.drop(index=rows_to_drop, inplace=True)



# Convert power in Watt to kiloWatt
laadpaaldata['TotalEnergy'] = round((laadpaaldata['TotalEnergy'] / 1000), 2)
laadpaaldata['MaxPower'] = round(laadpaaldata['MaxPower'] / 1000, 2)
# Efficiency calculation
laadpaaldata['Efficiency'] = (round((laadpaaldata['ChargeTime'] / laadpaaldata['ConnectedTime']) * 100, 2))
laadpaaldata['Avg-power'] = round((laadpaaldata['TotalEnergy'] / laadpaaldata['ChargeTime']), 2)


# TODO drop unnecessary columns

# TODO merge data

# Streamlit dashboard code
# Create two columns for the title and datepicker
title_col, datepicker_col = st.columns(2)
# Get the first and last date of the data to limit datapicker entries
start_date = laadpaaldata['Started'].min()
end_date = laadpaaldata['Ended'].max()

with title_col:
    st.title('Elektrische mobiliteit & laadpalen')
# Create Datepicker element
with datepicker_col:
    date = st.date_input(
        "Selecteer periode",
        (start_date, end_date),
        start_date,
        end_date
    )
# Fill variables from datepicker tuple
try:
    filter_start, filter_end = date
except ValueError:
    with st.spinner("Even denken.."):
        time.sleep(10)
    st.stop()
# Subset Dataframe based on datepicker
filtered_data = laadpaaldata[(laadpaaldata['Started'] >= pd.to_datetime(filter_start))
                             & (laadpaaldata['Ended'] <= pd.to_datetime(filter_end))]


# Container 2: Metrics
metric1, metric2, metric3, metric4 = st.columns(4)
# Get average charging time
charge_time = (filtered_data['ChargeTime'].mean()) * 60
connected_time = filtered_data['ConnectedTime'].mean() * 60
# Convert to hours and minutes
hours_charge, minutes_charge = divmod(charge_time, 60)
hours_conn, minutes_conn = divmod(connected_time, 60)

consumption = filtered_data['TotalEnergy'].sum()
avg_eff = filtered_data['Efficiency'].mean()

# Compute value to kWh or MWh based on the consumption
def compute_kW(kW):
    if kW == 0:
        return f" { 0.0 } MWh"
    elif kW > 0:
        if math.floor(math.log10(abs(kW))) >= 3:
            return f" {round((kW / 1000), 2)} MWh"
        else:
            return f" {round(kW, 2)} kWh"
    else:
        if math.floor(math.log10(abs(kW))) >= 3:
            return f" {round((kW / 1000), 2)} MWh"
        else:
            return f" {round(kW, 2)} kWh"


metric1.metric(
    label='Gem. Laadtijd',
    value=f" {int(hours_charge)} uur {int(minutes_charge)} min",
    delta=f"{int(hours_charge) - int(st.session_state['charge_hours'])} uur {int(minutes_charge) - int(st.session_state['charge_minutes'])} min",
    delta_color='off'
)
metric2.metric(
    label='Gem. Tijd aan de laadpaal',
    value=f" {int(hours_conn)} uur {int(minutes_conn)} min",
    delta=f"{int(hours_conn) - int(st.session_state['conn_hours'])} uur {int(minutes_conn) - int(st.session_state['conn_minutes'])} min",
    delta_color='off'
)
metric3.metric(
    label='Gem. Efficientie',
    value=f"{round(avg_eff, 2)} %",
    delta=f"{round(avg_eff - st.session_state['efficiency'], 2)}%"
)
metric4.metric(
    label='Totaal Opgeladen',
    value=compute_kW(consumption),
    delta=compute_kW((consumption - st.session_state['consumption']))
)
# Container 3: Charts
print(laadpaaldata)
fig_col1, fig_col2 = st.columns(2)
with fig_col1:
    st.markdown('### Relatie tussen geladen vermogen en max. geleverd vermogen')
    fig_scat = px.scatter(filtered_data, x='MaxPower', y='TotalEnergy', color='Efficiency')
    fig_scat.update_layout(
        xaxis_title='Maximaal gevraagd vermogen in kWh',
        yaxis_title='Geladen vermogen in kWh'
    )
    st.plotly_chart(fig_scat, theme='streamlit')

    # st.line_chart(df_grouped_day, y='TotalEnergy')
with fig_col2:
    st.markdown('### Efficiency occurrence')
    fig = px.histogram(filtered_data, x='Efficiency', nbins=10)
    fig.update_xaxes(range=[0, 100], title='Efficiency')
    st.plotly_chart(fig)

fig_col3, fig_col4 = st.columns(2)
with fig_col3:
    st.markdown('### Relatie tussen de laadtijd en het gemiddelde laadvermogen')
    fig_scat2 = px.scatter(filtered_data, y='Avg-power', x='ChargeTime', color='Efficiency', color_continuous_scale="greens")
    fig_scat2.update_layout(
        xaxis_title='Tijd aan het laden',
        yaxis_title='Gemiddeld vermogen in kWh'
    )
    st.plotly_chart(fig_scat2)
with fig_col4:
    st.markdown('### Power kW Distribution')
    PowerKwBox = px.box(openchargemap, y='PowerKW')
    st.plotly_chart(PowerKwBox)

st.session_state['efficiency'] = avg_eff
st.session_state['consumption'] = consumption
st.session_state['charge_hours'] = hours_charge
st.session_state['charge_minutes'] = minutes_charge
st.session_state['conn_hours'] = hours_conn
st.session_state['conn_minutes'] = minutes_conn

auto_brandstof = pd.read_csv("auto_brandstof.csv")

auto_brandstof = auto_brandstof.rename(columns={'Datum eerste toelating DT': 'toelating_datum',
                        'Vervaldatum APK DT': 'apk_datum',
                        'Brandstof omschrijving': 'brandstof'})

# print(df.isnull().sum())
auto_brandstof = auto_brandstof.dropna(axis=0)

auto_brandstof['apk_datum'] = pd.to_datetime(auto_brandstof['apk_datum'])
auto_brandstof['toelating_datum'] = pd.to_datetime(auto_brandstof['toelating_datum'])

auto_brandstof['apk_datum'] = auto_brandstof['apk_datum'].dt.strftime('%Y-%m')
auto_brandstof['toelating_datum'] = auto_brandstof['toelating_datum'].dt.strftime('%Y')

# Groepeer de gegevens op 'brandstof' en 'toelating_datum' en bereken de som
result_auto_brandstof = auto_brandstof.groupby(['brandstof', 'toelating_datum']).size().reset_index()
result_auto_brandstof = result_auto_brandstof.rename(columns={0:'aantal_auto'})

fig_col5, fig_col6 = st.columns(2)

with fig_col5:
    st.markdown("### Aantallen auto's per brandstof per jaar")
    fig = px.line(result_auto_brandstof, x="toelating_datum", y='aantal_auto', title='Aantallen auto per brandstof per jaar', color='brandstof')
    fig.update_xaxes(title_text='Toelating Datum')
    fig.update_yaxes(title_text='Aantal auto')
    st.plotly_chart(fig)

with fig_col6:
    st.markdown("### Voorspelling elektrische auto's")
#barchart auto brandstof per merk
#komt er nog

