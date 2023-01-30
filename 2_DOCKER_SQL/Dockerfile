FROM python:3.9

RUN pip install pandas python-dotenv sqlalchemy psycopg2

WORKDIR /app
COPY ingest_data.py ingest_data.py
COPY yellow_tripdata_2021-01.csv output.csv

ENTRYPOINT [ "python", "ingest_data.py"]