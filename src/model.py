import numpy as np
import pandas as pd
from pandas.api.types import is_numeric_dtype, is_integer_dtype
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
import joblib
from os.path import exists
from sklearn.impute import SimpleImputer


COLS = ['onRoadOld', 'onRoadNow', 'years', 'km', 'rating', 'condition', 'economy', 'topSpeed',
            'horsePower', 'torque']
'''===============================Data Preparation and Train model====================================='''

"""
input: path for the data set 
return the raw DataFrame
"""
def load_data(url = '../dataset/train_df.csv'):
    try:
        data = pd.read_csv(url)
        cols=COLS+['currentPrice']
        df = data[cols]
        return df
    except IOError as e:
        print(e)


# get an array of median value for each column, and saved as joblib file
def get_imputer(X : pd.DataFrame):
    imputer = SimpleImputer(missing_values=np.nan, strategy='median')
    imputer.fit(X)
    joblib.dump(imputer, 'models/imputer.joblib')
    return imputer


# train the standard scaler with training data, and save as joblib file
def get_scaler(X: pd.DataFrame):
    std_scaler =StandardScaler()
    std_scaler.fit(X)
    joblib.dump(std_scaler, 'models/scaler.joblib')
    return std_scaler


# Train a linear regression model with preprocessed data, and save the trained model with joblib
def get_model(X : pd.DataFrame, y: pd.Series):
    lr = LinearRegression()
    lr.fit(X, y)
    joblib.dump(lr, 'models/lr_model.joblib')
    return lr


"""
Train a new model
input: path for the data set 
Prepare the data and train the linear regression model with the data
return the trained model result
"""
def train_model():
    # Load data
    df = load_data()

    # Split data: X and y
    y = df['currentPrice']
    X = df.drop(['currentPrice'],axis=1)

    # Fit imputer
    get_imputer(X)

    # Scaling the X data
    scaler = get_scaler(X)
    X_ss = pd.DataFrame(scaler.transform(X), columns=X.columns)

    # Train the model
    lr = get_model(X_ss, y)

    return lr


"""
Re_train a model
input: path for the data set 
Prepare the data and train the linear regression model with the data
return the trained model result
"""
def retrain_model(path : str):
    # Load data
    df = load_data(path)

    # Split data: X and y
    y = df['currentPrice']
    X = df.drop(['currentPrice'],axis=1)

    # Scaling the X data
    scaler = get_scaler(X)
    X_ss = pd.DataFrame(scaler.transform(X), columns=X.columns)

    # Load and retrain the model
    lr = joblib.load('models/lr_model.joblib')
    lr.fit(X_ss, y)
    joblib.dump(lr, 'models/lr_model.joblib')

    return lr

'''===============================inference process====================================='''

# transform the X DataFrame with trained scaler
def scaler_transform(X: pd.DataFrame):
    scaler = joblib.load('models/scaler.joblib')
    X_ss = pd.DataFrame(scaler.transform(X), columns=X.columns)
    return X_ss

def imputer_transform(X: pd.DataFrame):
    imputer = joblib.load('models/imputer.joblib')
    X_imputed = pd.DataFrame(imputer.transform(X), columns=X.columns)
    return X_imputed


'''
Input: raw DataFrame, 
preprocessing the data, fill up null value with saved median value if neccessary, scale the data with saved scaler
Output: prediction result for car price
'''
def make_predict(X: pd.DataFrame):

    X = imputer_transform(X)
    X_ss = scaler_transform(X)
    lr = joblib.load('models/lr_model.joblib')
    y_pred = lr.predict(X_ss)
    y_pred[y_pred<0] = 0
    return y_pred


'''=============================================Data Ingestion=================================================='''
'''
check if the one sample data set has correct form for ML model
'''
def data_verification(df : pd.DataFrame):
    # check if the dataframe has shape of 1 row and 10 columns, and columns name are as required
    if (df.shape != (1,10)) | (sorted(df.columns.to_list) != sorted(COLS)):
        return False

    # years value should be between 0 and 10
    if not (is_integer_dtype(df['years']) and (0 <= df.loc[0,'years'] <= 10)):
        return False

    # rating value should be between 1 and 6
    if not (is_integer_dtype(df['rating']) and (1 <= df.loc[0,'rating'] <= 6)):
        return False

    # condition value should be between 1 and 10
    if not (is_integer_dtype(df['condition']) and (1 <= df.loc[0,'condition'] <= 10)):
        return False

    # economy value should be between 5 and 20
    if not (is_integer_dtype(df['economy']) and (5 <= df.loc[0,'economy'] <= 20)):
        return False

    # on road old value should be between 400000 and 800000
    if not (is_numeric_dtype(df['on road old']) and (400000 <= df.loc[0,'on road old'] <= 800000)):
        return False

    # on road now value should be between 600000 and 1000000
    if not (is_numeric_dtype(df['on road now']) and (600000 <= df.loc[0,'on road now'] <= 1000000)):
        return False

    # km value should be between 0 and 200000
    if not (is_numeric_dtype(df['km']) and (0 <= df.loc[0,'km'] <= 200000)):
        return False

    # top speed value should be between 120 and 250
    if not (is_numeric_dtype(df['top speed']) and (120 <= df.loc[0,'top speed'] <= 250)):
        return False

    # hp value should be between 40 and 140
    if not (is_numeric_dtype(df['hp']) and (40 <= df.loc[0,'hp'] <= 140)):
        return False

    # torque value should be between 50 and 160
    if not (is_numeric_dtype(df['torque']) and (50 <= df.loc[0,'torque'] <= 160)):
        return False

    else:
        return True


# Run the main function only when there is need to re-train the model
if __name__ == '__main__':
    # set the path to save the trained model result
    filepath = 'models/lr_model.joblib'
    # check if the lr_model.sav file already exist, if yes, ask if re_train the model
    if exists(filepath):
        answer = input('The trained model file already exists, do you want to train the model with new data? Y/N')
        if answer == 'Y':
            data_path = input('Please select your data (enter your data path: ')
            retrain_model(data_path)

    else:
        train_model()
