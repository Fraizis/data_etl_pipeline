import csv
import json
import logging
from typing import Any

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
    CREATE TABLE IF NOT EXISTS country_happiness (
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
        logging.info(f'Executed query: {q}')
        cur.close()
        psql_conn.commit()

    except (Exception, psycopg2.DatabaseError) as error:
        logging.error(error)


def extract_transform_data(path) -> list[Any]:
    """
    Country name,
    Regional indicator,
    Ladder score,
    Social support,
    Healthy life expectancy,
    Freedom to make life choices,
    Perceptions of corruption
    """
    transform_list = []

    with open(path, mode='r', newline='', encoding='utf-8') as csvfile:
        data = csv.DictReader(csvfile)

        for row in data:
            logging.info(f"Transforming data: {row['Country name']}, {row['Regional indicator']},"
                         f"{row['Ladder score']}, {row['Social support']}, {row['Healthy life expectancy']}, "
                         f"{row['Freedom to make life choices']}, {row['Perceptions of corruption']}")
            transform_list.append(
                (
                    row['Country name'], row['Regional indicator'], row['Ladder score'],
                    row['Social support'], row['Healthy life expectancy'],
                    row['Freedom to make life choices'], row['Perceptions of corruption']
                )
            )

    return transform_list


def load_country(data, psql_conn):
    q = """
    insert into country_happiness (
        country_name,
        regional_indicator,
        ladder_score,
        social_support,
        healthy_life_expectancy,
        freedom_to_make_life_choices,
        perceptions_of_corruption
    ) 
    values (%s, %s, %s, %s, %s, %s, %s)
    """
    try:
        cur = psql_conn.cursor()
        logging.info(f'Executed query: \n {q}')

        cur.executemany(q, data)
        psql_conn.commit()
        logging.info('Insert complete.')

        cur.close()
        psql_conn.close()
        logging.info('Cursor and connection closed.')

    except (Exception, psycopg2.DatabaseError) as error:
        logging.error(error)


def etl_pipeline(path, psql_conn):
    data = extract_transform_data(path)
    load_country(data, psql_conn)
