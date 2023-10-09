import streamlit as st
import pandas as pd
from ydata_profiling import ProfileReport
from streamlit_pandas_profiling import st_profile_report
from st_pages import add_page_title
from main import laadpaaldata, voertuigen

# Init page - Streamlit pages
add_page_title()


# Initialize reports
report_1 = ProfileReport(laadpaaldata, title='Laadpaal Data Report')
report_2 = ProfileReport(voertuigen, title='Elektrische voertuigen data report')

# Cache expensive functions
@st.cache_data(experimental_allow_widgets=True)
def createProfileReport(option):
    if option == 'Laadpaal':
        report = report_1
    else:
        report = report_2
    return st_profile_report(report)

option = st.selectbox('Kies een dataset...', ('Laadpaal', 'Elektrische voertuigen'))

# Call (cached) function to diplay profile report
createProfileReport(option)

