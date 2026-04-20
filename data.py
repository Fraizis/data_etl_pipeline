import logging

import psycopg2

user_data = {
    'user': 'postgres',
    'password': 'postgres',
    'host': 'localhost',
    'db_name': 'db'
}

path_to_jar = '"path_to_driver"/postgresql-42.7.10.jar'

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logging.warning('Start program and logger.')


def psql_connection(user, password, host, db_name):
    conn = None

    try:
        logging.info('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(user=f'{user}', password=f'{password}', host=f'{host}', database=f'{db_name}')

        cur = conn.cursor()

        cur.execute('SELECT version()')
        ver_db = cur.fetchone()

        logging.info(f'PostgreSQL database version: ')
        logging.info(ver_db)
        return conn

    except (Exception, psycopg2.DatabaseError) as error:
        logging.error(error)
