import streamlit as st
import pandas as pd
import requests
import json
from fastapi.encoders import jsonable_encoder
from fastapi import File, UploadFile
from io import StringIO
from csv import reader


# Page Headers
st.text('Dont Know how much your next car would cost? ')
st.subheader('Say No more!!  Predict the cost of the Fairly Used car prices')

# Page Tabs creation
tab1, tab2, tab3 = st.tabs(["Input Car Features", "Upload Feature Document", "View Past Predictions"])

# User Input Tab  specification
with tab1: 

    # User Input Form
    with st.form('user_input'):
            st.subheader('Fill in the details')
            onRoadOld = st.number_input('On Road Old',step=1)
            onRoadNow = st.number_input('On Road Now',step=1)
            years = st.number_input('Years',min_value=1, max_value=20)
            km = st.number_input('Km',step=1)
            rating = st.number_input('Rating',min_value=1, max_value=5)
            condition = st.number_input('Condition', min_value=1, max_value=10)
            economy = st.number_input('Economy',min_value=5, max_value=20)
            topSpeed = st.number_input('Top Speed', min_value=100, max_value=300)
            horsePower = st.number_input('Horse Power', min_value=50, max_value=200)
            torque = st.number_input('Torque', min_value=20, max_value=200)

            # Dictionary of User Input
            data ={
            'onRoadOld': onRoadOld,
            'onRoadNow': onRoadNow,
            'years':years,
            'km': km,
            'rating': rating,
            'condition': condition,
            'economy': economy,
            'topSpeed': topSpeed,
            'horsePower': horsePower,
            'torque': torque
            }

            submitted = st.form_submit_button("Submit")
            # On submit event for user input
            if submitted:
                response = requests.post("http://127.0.0.1:8000/user_input", json=data)
                prediction = response.text
                st.success('The car may likely cost  {} '.format(prediction))
                st.balloons()

with tab2:
    # Page Header
    st.header('Upload a CSV or Excel file with used Cars info')

    # File Input
    uploaded_file = st.file_uploader("Choose a file", type="csv")
    if uploaded_file is not None:
        byte_data = uploaded_file.getvalue()
        file_data = pd.read_csv(uploaded_file)
        st.dataframe(file_data)
 

    # Submit Button
    submit_file = st.button("Submit")

    # On submit events
    if submit_file:
        response = requests.post("http://127.0.0.1:8000/file", files={"file": byte_data})
        st.write(response.status_code)
        data_dict = json.loads(response.text)    
        d = pd.read_csv(StringIO(data_dict["content"]), sep=",")
        st.write(d)

        

with tab3:
        st.header("View Predictions")

        with st.form('search_criteria'):
            st.subheader('You want to know the previous prediction record? Please enter your searching criteria: ')
            year = st.number_input('Year', min_value=1, max_value=20)
            search_text = {"years":year}

            submitted = st.form_submit_button("Confirm Search")
            # On submit event for user input
            if submitted:
                response = requests.post("http://127.0.0.1:8000/search",  json=search_text)
                results = json.loads(response.text)
                df_results = pd.read_csv(StringIO(results["result"]), sep=",")
                st.write(df_results)
