from scrap_games.load_data import create_table, load_cards
from scrap_games.scrap_cards import scrap_card
from scrap_games.settings import psql_connection

if __name__ == '__main__':
    conn = psql_connection()
    create_table(conn)
    data = scrap_card()
    load_cards(data, conn)
