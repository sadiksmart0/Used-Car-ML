import numpy as np
from datetime import datetime
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
import joblib
from os.path import exists
from sklearn.impute import SimpleImputer
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, mean_absolute_error
import mlflow


features = ['onRoadOld', 'onRoadNow', 'years', 'km', 'rating', 'condition', 'economy', 'topSpeed',
            'horsePower', 'torque']


############################   Data Preparation and Train model #####################
def load_data(url = 'C:/Users/A.M. MUKTAR/Used-Car-ML/dataset/train_df.csv'):
    try:
        data = pd.read_csv(url)
        cols=features+['price']
        df = data[cols]
        return df
    except IOError as e:
        print(e)


##################  IMPUTE MISSING DATA   ###########################################
def get_imputer(X : pd.DataFrame):
    imputer = SimpleImputer(missing_values=np.nan, strategy='median')
    imputer.fit(X)
    #joblib.dump(imputer, 'models/imputer.joblib')
    return imputer


#####################  TRAIN SCALER     #################################################
def get_scaler(X: pd.DataFrame):
    std_scaler =StandardScaler()
    std_scaler.fit(X)
    #joblib.dump(std_scaler, 'models/scaler.joblib')
    return std_scaler


########################  SPLIT TRAIN & TEST DATA  ########################################
def train_split():
    df = load_data()
    y = df.price
    X = df.drop(['price'], axis=1)
    get_imputer(X)
    scaler = get_scaler(X)
    X = scaler.transform(X)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=66)
    return X_train, X_test, y_train, y_test


#########################   TRAIN MODEL        ##############################################
def train_model(X : pd.DataFrame, y: pd.Series):
    classifier = LinearRegression()
    classifier.fit(X, y)
    #joblib.dump(lr, 'models/lr_model.joblib')
    return classifier

#########################   PREDICT MODEL        ##############################################
def predict_on_test(model, X_test):
    y_pred = model.predict(X_test)
    return y_pred


#########################   METRICS        ##############################################
def get_metrics(y_test, y_pred):
    mse = mean_squared_error(y_test, y_pred)
    rmse = mean_squared_error(y_test, y_pred, squared=False)
    mae = mean_absolute_error(y_test, y_pred)
    return {'TEST MSE': mse, 'TEST RMSE':rmse, 'TEST MAE':mae}





##################  MFLOW   ##############################################
def log_all():
    training_timestamp = datetime.now().strftime('%Y-%m-%d, %H:%M:%S')
    experiment_name = 'exp_1'
    mlflow.set_experiment(experiment_name)
    with mlflow.start_run(run_name=f'model_{training_timestamp}'):
        mlflow.autolog()
        X_train, X_test, y_train, y_test = train_split()
        model = train_model(X_train, y_train)
        cls = predict_on_test(model, X_test)
        metrics = get_metrics(y_test, cls)
        mlflow.log_metrics(metrics)
        # remote_server_uri = "http://127.0.0.1/:5000"
        # mlflow.set_tracking_uri(remote_server_uri)
    return