from scrap_games.load_data import parsing_pipeline
from scrap_games.scrap_cards import scrap_nintendo
from scrap_games.settings import psql_connection

if __name__ == '__main__':
    conn = psql_connection()
    data = scrap_nintendo()
    parsing_pipeline(data, conn)
