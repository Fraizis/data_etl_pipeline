import csv
import json
import logging
import psycopg2


def init_logger():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    logging.warning('Start program and logger.')


def psql_connection():
    conn = None
    try:
        logging.info('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(host='localhost', database='mydb', user='postgres', password='postgres')
        cur = conn.cursor()

        cur.execute('SELECT version()')
        ver_db = cur.fetchone()

        logging.info(f'PostgreSQL database version: ')
        logging.info(ver_db)
        return conn
    except (Exception, psycopg2.DatabaseError) as error:
        logging.error(error)


def create_table(psql_conn):
    """
    Country name,Regional indicator,Ladder score,Social support,Healthy life expectancy,
    Freedom to make life choices,Perceptions of corruption
"""
    q = """
    CREATE TABLE IF NOT EXISTS sales (
        id SERIAL PRIMARY KEY,
        country_name VARCHAR(50) NOT NULL,
        regional_indicator VARCHAR(50) NOT NULL,
        ladder_score DECIMAL,
        social_support DECIMAL,
        healthy_life_expectancy DECIMAL,
        freedom_to_make_life_choices DECIMAL,
        perceptions_of_corruption DECIMAL
    )
    """
    try:
        cur = psql_conn.cursor()

        cur.execute(q)
        cur.close()
        psql_conn.commit()

    except (Exception, psycopg2.DatabaseError) as error:
        logging.error(error)


def insert_country():
    q = """
    insert into country_happiness (
    ) values (%s, %s, %s, %s, %s, %s, %s)
    """




def extract_data_from_csv(path, psql_conn):
    """
    Country name,
    Regional indicator,
    Ladder score,
    Social support,
    Healthy life expectancy,
    Freedom to make life choices,
    Perceptions of corruption
    """
    with open(path, mode='r', newline='', encoding='utf-8') as csvfile:
        data = csv.DictReader(csvfile)
        # insert_country()
        # writer = csv.writer('output.csv')
        for row in data:
            logging.info(f'Processing country: {row}')
            insert_country(row)
        #     print(row['Country name'],
        #           row['Regional indicator'],
        #           row['Ladder score'],
        #           row['Social support'],
        #           row['Healthy life expectancy'],
        #           row['Freedom to make life choices'],
        #           row['Perceptions of corruption']
        #           )
            # writer.writerow(row)

        # print(data)
        # for row in data:
        #     # print(row)
        #     print(row["Country name"], row["Regional indicator"], row["Ladder score"])


def insert_tables_from_csv(data):


def json_handle(path: str, data):
    with open(path, mode='w', encoding='utf-8') as jsonfile:
        json.dump(data, jsonfile, indent=4)



extract_data_from_csv('2020.csv')
