import csv
import json

import pandas as pd

from walmart_analysis.load_data import create_table, save_to_db
from walmart_analysis.settings import psql_connection, CSV_FILE

if __name__ == '__main__':
    conn = psql_connection()
    create_table(conn)
    save_to_db(conn, CSV_FILE)
    # df = pd.read_csv(CSV_FILE)  # или pd.read_csv('path_to_file.csv')
    # print(df.dtypes)
    # with open('output.json', 'r') as f:
    #     data = json.load(f)
    #     print(data[0])
