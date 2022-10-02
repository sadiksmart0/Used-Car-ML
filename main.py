from distutils.log import debug
import streamlit as st
from pickletools import float8
from fastapi import FastAPI
import pandas as pd
import uvicorn
import pickle
from pydantic import BaseModel
import json



# FastApi declaration
app = FastAPI(title='Used Car Price Predictions', version='1.0',
description='Linear Regression model is used for prediction')

# Validation of user and file data
class Data(BaseModel):
    onRoadOld: float 
    onRoadNow: float 
    years: float
    km: float
    rating: float
    condition: float
    economy: float
    topSpeed: float
    horsePower: float
    torque: float



# predict function  declaration for user input / file input
@app.post("/predict")
async def predict(data: Data):
    #Converting to dictionary and to dataframe
    data_dict = data.dict()
    df2 = pd.DataFrame.from_dict([data_dict])

    #model loading
    pickle_in = open("predict.pkl","rb")
    classifier = pickle.load(pickle_in)
    #model prediction
    prediction = classifier.predict(df2)
    return {"prediction": prediction[0]}



if __name__ == '__main__':
    uvicorn.run("main:app", host="127.0.0.1",port=8000, reload=True, debug=True)
    
