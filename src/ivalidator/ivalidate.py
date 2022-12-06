import pandas as pd
import pandera as pa
from pandera import DataFrameSchema, Column, Check
import smtplib


# import required module
from pathlib import Path
 
# assign directory
directory = 'C:/Users/A.M. MUKTAR/Used-Car-ML/data/folder_A'

#########################         Data validation checks    ##################################
schema = DataFrameSchema({
    "onRoadOld": Column(int, Check.in_range(10000,1000000)),
    "onRoadNow": Column(int, Check.in_range(10000,1000000)),
    "years": Column(int, Check.in_range(1, 10)),
    "km": Column(int, Check.in_range(1000,1000000)),
    "rating": Column(int, Check.in_range(1, 20)),
    "condition": Column(int, Check.in_range(1, 20)),
    "economy": Column(int, Check.in_range(1, 20)),
    "topSpeed": Column(int, Check.in_range(80, 500)),
    "horsePower": Column(int, Check.in_range(45, 500)),
    "torque": Column(int, Check.in_range(65, 300)),
    "currentPrice": Column(int, Check.in_range(100000,1000000)),
},coerce=True, strict=True, ordered=True)


#############    Fetch files from folder_A  ####################
files = Path(directory).glob('*.csv')

###########  Assign passed and failed files  ###################
passed = []
failed = []


################ EMAIL ##############################
def sendAlert(count):
    server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
    server.login("sadiksmart0@gmail.com", "pvnulgrlejhjfqwk")
    subject = 'Subject: VALIDATION ALERT'
    body = " files were found to be bad and could not be validated can be found in the failed folder"
    server.sendmail("Used-Car-ML@gmail.com", "assiddiquun001@gmail.com", f"{subject}\n\n{count}{body}")
    server.quit()

#####################    Data Quality Checks  #######################

def check_quality():
    for file in files:
        df = pd.read_csv(file, index_col=0, na_values=['(NA)']).fillna(0)
        df = df.apply(pd.to_numeric, errors='coerce')
        df.fillna(0, inplace=True)
        filepath = f'/c/Users/A.M. MUKTAR/Used-Car-ML/data/Passed/{Path(file).stem}.csv'
        filepath2 = f'/c/Users/A.M. MUKTAR/Used-Car-ML/data/Failed/{Path(file).stem}.csv'

        try:
            schema.validate(df, lazy=True)
            passed.append(df)
            df.to_csv(filepath, index=False)
        except pa.errors.SchemaErrors as exc:
            fail_case = exc.failure_cases
            percentage_pass = len(fail_case)/len(df)*100
            if percentage_pass <= 10:
                passed.append(df)
                df.to_csv(filepath, index=False)
            else:
                failed.append(df)
                df.to_csv(filepath2, index=False)
    return len(failed)

