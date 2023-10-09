import streamlit as st
import pandas as pd
from ydata_profiling import ProfileReport
from streamlit_pandas_profiling import st_profile_report
from st_pages import add_page_title

# Init page - Streamlit pages
add_page_title()

voertuigen = pd.read_csv('elektrischeVoertuigen.csv')

report = ProfileReport(voertuigen, title='Elektrische voertuigen data report')


@st.cache_data(experimental_allow_widgets=True)
def createProfileReport(_report):
    return st_profile_report(_report)


createProfileReport(report)
