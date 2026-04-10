import logging
import random

import psycopg2
from selenium import webdriver

user_agents = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36 OPR/129.0.0.0'
]

user_agent = random.choice(user_agents)

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--window-size=1920,1080")
chrome_options.add_argument(f"user-agent={user_agent}")

logging.basicConfig(
    filename='scrapping_nintendo.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def psql_connection():
    conn = None

    try:
        logger.info('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(host='localhost', database='mydb', user='postgres', password='postgres')
        cur = conn.cursor()

        cur.execute('SELECT version()')
        ver_db = cur.fetchone()

        logger.info(f'PostgreSQL database version: ')
        logger.info(ver_db)
        return conn

    except (Exception, psycopg2.DatabaseError) as error:
        logger.error(error)
