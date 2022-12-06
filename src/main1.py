
from fastapi import FastAPI
import pandas as pd
import uvicorn
from pydantic import BaseModel, validator
from typing import List, Optional
import numpy as np
from fastapi import File, UploadFile
from io import StringIO
from io import BytesIO
import model
from database import write_to_database
from database import get_from_database
import json
import datetime



class Test(BaseModel):
    hey: str

# BaseModel for searching criteria passed from streamlit
class Search(BaseModel):
    years: int
    

# # ===================================Declaring FASTAPI============================================

# FastApi declaration
app = FastAPI(title='Used Car Price Predictions', version='1.0',
              description='Linear Regression model is used for prediction')



# ===================================Validating File ============================================
class Data(BaseModel):
    onRoadOld: int
    onRoadNow: int
    years: int
    km: int
    rating: int
    condition: int
    economy: int
    topSpeed: int
    horsePower: int
    torque: int
    
    @validator('*')
    def is_String(cls, v):
        if type(v) == str:
            raise ValueError('value must be a number')
        return v


# # ===================================File Prediction============================================


def predict(data):
    #Validate data
    for index, row in data.iterrows():
        Data(**row)
    
    # make prediction
    pred_val = model.make_predict(data)
    return pred_val


# # ===================================USER PREDICTION END POINT FASTAPI============================================
@app.post("/user_input")
def user_predict(user_input: Data):
    data_dict = user_input.dict()
    # Converting to dictionary and to dataframe
    df = pd.DataFrame.from_dict([data_dict])  # type: ignore
    result = predict(df)
    df["predicted_price"] = result
    df['time'] = datetime.datetime.now()
    print(df)
    write_to_database(df)
    return {"result": df["predicted_price"]}
    



# # ===================================FILE PREDICTION END POINT FASTAPI============================================
@app.post("/file")
def file_prediction(file: UploadFile = File(...)):
    #Read file
    contents = file.file.read()
    data = BytesIO(contents)
    #Convert to dataframe
    df = pd.read_csv(data, sep=",")
    result = predict(df)
    df["predicted_price"] = result
    df['time'] = datetime.datetime.now()
    #Write to Database
    write_to_database(df)
    byteData = df.to_csv(index=False, encoding='utf-8').encode()
    return {"content": byteData}


#  ===================================SEARCH END-POINT FASTAPI============================================
@app.post("/search")
def search(search: Search):
    kword = search.years
    #get the query result from database with the keyword sending from streamlit app
    db_fetch = get_from_database(kword)
    byteData = db_fetch.to_csv(index=False, encoding='utf-8').encode()
    return {"result": byteData}


if __name__ == '__main__':
    uvicorn.run("main1:app", host="127.0.0.1", port=8000, reload=True)

