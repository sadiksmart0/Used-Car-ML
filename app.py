from turtle import width
import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image
from io import StringIO
import pickle
import requests
import json
import uvicorn
from fastapi import FastAPI
pickle_in = open("predict.pkl","rb")
classifier = pickle.load(pickle_in)

# FastApi Declaration
app = FastAPI()

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
            onRoadOld = st.number_input('On Road Old')
            onRoadNow = st.number_input('On Road Now')
            years = st.number_input('Years')
            km = st.number_input('Km')
            rating = st.number_input('Rating')
            condition = st.number_input('Condition')
            economy = st.number_input('Economy')
            topSpeed = st.number_input('Top Speed')
            horsePower = st.number_input('Horse Power')
            torque = st.number_input('Torque')
            submitted = st.form_submit_button("Submit")

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
            # On submit event for user input
            if submitted:
                response = requests.post("http://127.0.0.1:8000/predict", json=data)
                prediction = response.text
                st.success('The car may likely cost  {} '.format(prediction))
                st.balloons()
        
    

# File Input Tab Specification  

with tab2:

    # Page Header
    st.header('Upload a CSV or Excel file with used Cars info')

    # File Input
    with st.form("file_input"):
        uploaded_file = st.file_uploader("Choose a file", type="csv")
        if uploaded_file is not None:
            # To convert to a string based IO:
            stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
            
            # To read file as string:
            string_data = stringio.read()

            # Conversion Dataframe 
            dataframe = pd.read_csv(uploaded_file)
            st.dataframe(dataframe)
        #Submit Button
        submit_file = st.form_submit_button("Submit")
        result = []

        #On submit events
        if submit_file:
            # Converting dataframe to dictionary
            load = dataframe.to_dict(orient='records')

            #Looping through the dictionary
            for i in load:
                #Sending request
                response = requests.post("http://127.0.0.1:8000/predict", json=i,headers={"Content-Type": "application/json"})
                prediction = response.text

                # Appending response
                result.append(prediction)
    #Display list of result            
    st.title("Here is a List of your results")            
    st.write(result)
            

with tab3:
        st.header("View Predictions")
