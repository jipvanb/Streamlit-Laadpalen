import streamlit as st
import pandas as pd
from ydata_profiling import ProfileReport
from streamlit_pandas_profiling import st_profile_report
from st_pages import add_page_title
from main import laadpaaldata, voertuigen

# Init page - Streamlit pages
add_page_title()

# Data cleaning
laadpaaldata['Started'] = pd.to_datetime(laadpaaldata['Started'], format='%Y-%m-%d %H:%M:%S', errors='coerce')
laadpaaldata['Ended'] = pd.to_datetime(laadpaaldata['Ended'], format='%Y-%m-%d %H:%M:%S', errors='coerce')
laadpaaldata.dropna(subset=['Started'], inplace=True)
laadpaaldata.dropna(subset=['Ended'], inplace=True)

# Initialize reports
report_1 = ProfileReport(laadpaaldata, title='Laadpaal Data Report')
report = ProfileReport(voertuigen, title='Elektrische voertuigen data report')

# Cache expensive functions
@st.cache_data(experimental_allow_widgets=True)
def createProfileReport(_report):
    return st_profile_report(_report)

# Call (cached) function to diplay profile report
createProfileReport(report_1)
