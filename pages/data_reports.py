import streamlit as st
import pandas as pd
from ydata_profiling import ProfileReport
from streamlit_pandas_profiling import st_profile_report
from main import laadpaaldata, auto_brandstof, openchargemap



# Initialize reports
report_1 = ProfileReport(laadpaaldata, title='Laadpaal Data Report')
report_2 = ProfileReport(auto_brandstof, title='Voertuigen data Report')
report_3 = ProfileReport(openchargemap, title='Openchargemap data Report')

# Cache expensive functions
@st.cache_data(experimental_allow_widgets=True)
def createProfileReport(option):
    if option == 'Laadpaal':
        report = report_1
    elif option == 'Elektrische voertuigen':
        report = report_2
    elif option == 'Openchargemap':
        report = report_3
    return st_profile_report(report)

option = st.selectbox('Kies een dataset...', ('Laadpaal', 'Elektrische voertuigen', 'Openchargemap'))

# Call (cached) function to diplay profile report
createProfileReport(option)

