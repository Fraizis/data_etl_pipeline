import psycopg2

from scrap_games.settings import logger


def create_table(psql_conn):
    q = """
    CREATE TABLE IF NOT EXISTS nintendo_games (
        id SERIAL PRIMARY KEY,
        name VARCHAR(50),
        genres VARCHAR(50),
        rating DECIMAL,
        description TEXT,
        platform VARCHAR(50),
        price_eur DECIMAL,
        multiplayer VARCHAR(50),
        developer VARCHAR(50),
        img_url VARCHAR(200),
        date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """
    try:
        cur = psql_conn.cursor()

        cur.execute(q)
        logger.info(f'Executed query: {q}')
        cur.close()
        psql_conn.commit()

    except (Exception, psycopg2.DatabaseError) as error:
        logger.error(error)


def load_cards(data, psql_conn):
    q = """
    insert into nintendo_games (
        name, 
        genres, 
        rating, 
        description, 
        platform, 
        price_eur, 
        multiplayer, 
        developer,
        img_url
        ) 
    values (%s, %s, %s, %s, %s, %s, %s, %s, %s);
    """
    try:
        cur = psql_conn.cursor()
        logger.info(f'Executed query: \n {q}')

        cur.executemany(q, data)
        psql_conn.commit()
        logger.info('Insert complete.')

        cur.close()
        psql_conn.close()
        logger.info('Cursor and connection closed.')

    except (Exception, psycopg2.DatabaseError) as error:
        logger.error(error)
