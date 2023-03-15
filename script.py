# sample project https://docs.streamlit.io/library/get-started/create-an-app

import streamlit as st
import pandas as pd
import numpy as np

st.title('experimental graph with Q-Scope data')

DATE_COLUMN = 'current_date' # name of column for Y axis

DATA_URL = ('data/CO2_emissions_4.17.csv') #at 20221110_ExpertInnenWorkshop/20221110_ExpertInnenWorkshop/output_20221110_15-13-10_Runde1/emissions/

@st.cache_data #cache loaded data. at the next run, the streamlit will take the data from cache 
def load_data(nrows):
    data = pd.read_csv(DATA_URL, nrows=nrows)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis='columns', inplace=True)
    data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN].str[7:17]) # trimming date value
    return data

data_load_state = st.text('Loading data...')
data = load_data(10000)
data_load_state.text("Done! (using st.cache_data)")

if st.checkbox('Show raw data'):
    st.subheader('Raw data')
    st.write(data)

# create slider for specifying the number of data to show 
day_to_filter = st.slider('day', 0, len(data.index), 50) 

# create radio button
graph_types = ['line_chart', 'bar_chart']
selected_graph_type = st.radio('Graph type', graph_types)

# prepare pandas data
chart_data = data[[DATE_COLUMN, "building_household_emissions"]]
chart_data = chart_data[chart_data.index<day_to_filter] # select rows by the comparison with the slider value 

#toggle displayed graph based on selection
if selected_graph_type == 'line_chart':
    st.subheader('simple line chart')
    st.line_chart(chart_data, y="building_household_emissions")
else:
    st.bar_chart(chart_data, x= "current_date", y="building_household_emissions")
