import requests
import pandas as pd
import numpy as np
import plotly.express as px
import matplotlib.pyplot as plt
import streamlit as st

# load data
laadpaaldata = pd.read_csv('laadpaaldata.csv')
voertuigen = pd.read_csv('elektrischeVoertuigen.csv')
key = "b2451f45-7af1-4a46-a430-8496d6583401"
res = requests.get(f"https://api.openchargemap.io/v3/poi/?output=json&countrycode=NL&maxresults=10000&compact=true&verbose=false&key={key}")
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