import pandas as pd
import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from time import time

load_dotenv()

USER = os.getenv('USER')
PASSWORD = os.getenv('PASSWORD')
HOST = os.getenv('HOST')
PORT = os.getenv('PORT')
DB = os.getenv('DB')
TABLE_NAME = os.getenv('TABLE_NAME')

csv_name = 'output.csv'

connection = create_engine(
    f'postgresql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DB}')

df_iter = pd.read_csv(csv_name, iterator=True, chunksize=10_000)


df = next(df_iter)
df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)

df.head(0).to_sql(name=TABLE_NAME, con=connection, if_exists="replace")
df.to_sql(name=TABLE_NAME, con=connection, if_exists='append')

while True: 

    try:
        t_start = time()
    
        df = next(df_iter)

        df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
        df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)

        df.to_sql(name=TABLE_NAME, con=connection, if_exists='append')

        t_end = time()

        print('inserted another chunk, took %.3f second' % (t_end - t_start))

    except StopIteration:
        print("Finished ingesting data into the postgres database")
        break