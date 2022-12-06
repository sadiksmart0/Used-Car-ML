from sqlalchemy.ext.declarative import declarative_base
from dotenv import load_dotenv
import pandas as pd
from sqlalchemy import create_engine

  
################## CONNECTION STRING ###################
DATABASE_URL= 'postgresql+psycopg2://dsp:12345678@localhost:5432/usedcar'
engine = create_engine(DATABASE_URL)



#######  WRITE DATA TO DATABASE   ############
def write_to_database(df):
    df.to_sql('carprice', engine, if_exists='append', index=False)
    return

########  FETCH  FROM DATABASE    ############
def get_from_database(keyword)-> pd.DataFrame:
    search = pd.read_sql('carprice', engine)
    search = search[search["years"]==keyword]
    return search

