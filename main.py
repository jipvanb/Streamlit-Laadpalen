import requests
import pandas as pd
import numpy as np
import plotly.express as px
import matplotlib.pyplot as plt
import streamlit as st

# load data
laadpaaldata = pd.read_csv('laadpaaldata.csv')
# voertuigen = pd.read_csv('elektrischeVoertuigen.csv')
# TODO change request (maxresults, key)
res = requests.get(
    "https://api.openchargemap.io/v3/poi/?output=json&countrycode=NL&maxresults=100&compact=true&verbose=false&key=93b912b5-9d70-4b1f-960b-fb80a4c9c017")
data = res.json()
openchargemap = pd.json_normalize(data)
df4 = pd.json_normalize(openchargemap.Connections)
df5 = pd.json_normalize(df4[0])
openchargemap = pd.concat([openchargemap, df5], axis=1)
openchargemap.drop(columns=['Connections'], inplace=True)


# TODO clean data
# Drop two data rows with incorrect dates --> 2018 is not a leap year?
laadpaaldata.drop([1731, 1732], axis=0, inplace=True)
# Converting strings to datetime series
laadpaaldata['Started'] = pd.to_datetime(laadpaaldata['Started'], format='%Y-%m-%d %H:%M:%S')
laadpaaldata['Ended'] = pd.to_datetime(laadpaaldata['Ended'], format='%Y-%m-%d %H:%M:%S')

# TODO drop unnecessary columns

# TODO merge data