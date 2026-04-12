import csv


def write_csv_urls(path):
    fields = [
        'name', 'genres', 'rating', 'description', 'platform',
        'price_eur', 'multiplayer', 'developer', 'img_url'
    ]
    data = {
        'name': 'name', 'genres': 'genres', 'rating': 'rating',
        'description': 'description', 'platform': 'game_pl',
        'price_eur': 'price_eur', 'multiplayer': 'mp',
        'developer': 'developer', 'img_url': 'img_url'
    }

    with open(path, mode='w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fields)
        writer.writerow(data)

        # writer = csv.writer(csvfile)
        # writer.writerow(row)
        # links = scrap_cards(URL)
        #
        # for l in links:
        #     writer.writerow(l)
    # logger.info(f'Writed to csv: {row}')


def load_data_to_db(path):
    transform_list = []

    with open(path, mode='r', newline='', encoding='utf-8') as csvfile:
        data = csv.DictReader(csvfile)
        for row in data:
            # logger.info(f"Transforming data: {row['Country name']}, {row['Regional indicator']},"
            #             f"{row['Ladder score']}, {row['Social support']}, {row['Healthy life expectancy']}, "
            #             f"{row['Freedom to make life choices']}, {row['Perceptions of corruption']}")
            transform_list.append(
                [
                    row['name'], row['genres'], row['rating'], row['description'],
                    row['platform'], row['price_eur'], row['multiplayer'], row['developer'], row['img_url']
                ]
            )
        # print(transform_list)

    return transform_list
