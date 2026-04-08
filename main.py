import csv
import json


from prepare_connection import init_logger, psql_connection, create_table

if __name__ == '__main__':
    init_logger()
    conn = psql_connection()
    create_table(conn)


    # with open('MS_Clients.csv', mode='r', newline='', encoding='utf-8-sig') as csvfile:
    #     data = csv.DictReader(csvfile)
    #     for row in data:
    #         print(row["ClientID"], row["ClientName"], row["Gender"])
        # for i in data:
        #     print(i)
        # print(data)

    # with open('MS_Clients.json', mode='w', encoding='utf-8-sig') as jsonfile:
    #     json.dump(data, jsonfile, indent=4)
