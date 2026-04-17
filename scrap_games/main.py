from data import psql_connection, user_data
from scrap_games.load_data import create_table, load_cards
from scrap_games.scrap_cards import scrap_card

if __name__ == '__main__':
    conn = psql_connection(**user_data)
    if conn:
        create_table(conn)
        data = scrap_card()
        load_cards(data, conn)
