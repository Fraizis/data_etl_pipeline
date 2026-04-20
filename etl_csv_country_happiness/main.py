from data import user_data, psql_connection
from etl_csv_country_happiness.load_data import create_table, etl_pipeline
from etl_csv_country_happiness.settings import CSV_FILE


def etl_happiness(**data):
    conn = psql_connection(**data)
    if conn:
        create_table(conn)
        etl_pipeline(CSV_FILE, conn)


if __name__ == '__main__':
    etl_happiness(**user_data)
