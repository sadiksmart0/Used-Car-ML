import numpy as np
import pandas as pd
from pandas.api.types import is_numeric_dtype, is_integer_dtype
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
import joblib
from os.path import exists
from sklearn.impute import SimpleImputer
import requests
import json
 



##################   inference process       ##########################################

# transform the X DataFrame with trained scaler
def scaler_transform(X: pd.DataFrame):
    scaler = joblib.load('models/scaler.joblib')
    X_ss = pd.DataFrame(scaler.transform(X), columns=X.columns)
    return X_ss

def imputer_transform(X: pd.DataFrame):
    imputer = joblib.load('models/imputer.joblib')
    X_imputed = pd.DataFrame(imputer.transform(X), columns=X.columns)
    return X_imputed


##################   RUN PREDICTION      ##################################################
def make_predict(X: pd.DataFrame):
    X = imputer_transform(X)
    X_ss = scaler_transform(X)
    endpoint = 'http://127.0.0.1:1234/invocations'
    data = X_ss.values.tolist()
    inference = {"dataframe_records": data}
    response = requests.post(endpoint, json=inference)
    prediction = json.loads(response.text)
    y_pred = pd.DataFrame(prediction["predictions"])
    return y_pred


