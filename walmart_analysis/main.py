import pandas as pd

from walmart_analysis.add_column_logic import add_time_day_month
from walmart_analysis.load_data import create_table, save_to_db
from walmart_analysis.settings import psql_connection, CSV_FILE

if __name__ == '__main__':
    conn = psql_connection()
    create_table(conn)
    # save_to_db(conn, CSV_FILE)
    add_time_day_month(conn)
