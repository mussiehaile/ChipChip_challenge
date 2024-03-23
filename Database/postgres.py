import psycopg2
import pandas as pd
import os
from config.config_static_files import *

def Database_connect():
        conn = psycopg2.connect(
            host="localhost",
            port="5432",
            database=ConfigStaticFiles.DB_DATABASE,
            user=ConfigStaticFiles.DB_USER,
            password=ConfigStaticFiles.DB_PASSWORD
        )
        return conn



# function for handling extraction from db 
def database_extractor(table_name):

    conn = Database_connect()

    # SQL query to retrieve data from a table
    query = f"SELECT * FROM {table_name}"

    # Read data into a Pandas DataFrame
    df = pd.read_sql_query(query, conn)

    # Close the database connection
    conn.close()
    return df



def databse_query(product_id):
        if product_id:
            query = f"SELECT * FROM group_deals WHERE product_id = {product_id}"
        else:
            query = "SELECT * FROM group_deals"
        return query