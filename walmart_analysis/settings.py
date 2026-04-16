import logging
import os

import psycopg2

FILE_PATH = os.path.dirname(__file__)
CSV_FILE = FILE_PATH + '/WalmartSalesData.csv.csv'

USER = 'USER'
PASSWORD = 'PASSWORD'
HOST = 'HOST'
DB_NAME = 'DB_NAME'

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def psql_connection():
    conn = None

    try:
        logger.info('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(user=f'{USER}', password=f'{PASSWORD}', host=f'{HOST}', database=f'{DB_NAME}')

        cur = conn.cursor()

        cur.execute('SELECT version()')
        ver_db = cur.fetchone()

        logger.info(f'PostgreSQL database version: ')
        logger.info(ver_db)
        return conn

    except (Exception, psycopg2.DatabaseError) as error:
        logger.error(error)
