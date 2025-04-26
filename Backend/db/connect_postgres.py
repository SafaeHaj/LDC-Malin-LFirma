import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

load_dotenv()

db_usr = os.getenv("DB_USR")
db_pwd = os.getenv("DB_PWD")
db_host = os.getenv("DB_HOST")
db_port = os.getenv("DB_PORT")
db_name = os.getenv("DB_NAME")

engine = create_engine(f'postgresql://{db_usr}:{db_pwd}@{db_host}:{db_port}/{db_name}')

def connect_to_db():
    try:
        connection = engine.connect()
        print("Connection to the database was successful.")
        return connection
    except Exception as e:
        print(f"An error occurred while connecting to the database: {e}")
        return None

def check_data(connection, table_name):
    try:
        result = connection.execute(text(f"SELECT * FROM {table_name} LIMIT 5"))
        for row in result:
            print(row)
    except Exception as e:
        print(f"An error occurred while querying the table: {e}")

