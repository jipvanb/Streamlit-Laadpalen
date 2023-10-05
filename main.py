import requests
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# load data
laadpaaldata = pd.read_csv('laadpaaldata.csv')
voertuigen = pd.read_csv('elektrischeVoertuigen.csv')
# TODO change request (maxresults, key)
res = requests.get("https://api.openchargemap.io/v3/poi/?output=json&countrycode=NL&maxresults=100&compact=true&verbose=false&key=93b912b5-9d70-4b1f-960b-fb80a4c9c017")
data = res.json()
openchargemap = pd.json_normalize(data)
df4 = pd.json_normalize(openchargemap.Connections)
df5 = pd.json_normalize(df4[0])
openchargemap = pd.concat([openchargemap, df5], axis=1)
openchargemap.drop(columns=['Connections'], inplace=True)

# TODO clean data

# TODO drop unnecessary columns

# TODO merge data