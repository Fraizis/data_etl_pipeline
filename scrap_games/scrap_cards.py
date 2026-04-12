import random
from time import sleep
import requests
from bs4 import BeautifulSoup

from scrap_games.settings import logger, URL, user_agents


def scrap_card():
    p = 2999
    cards = []

    while True:
        user_agent = random.choice(user_agents)
        print(user_agent)
        url = f'{URL}{p}'

        headers = {'User-Agent': user_agent}
        logger.warning(f'Start parsing: {url}')

        response = requests.get(url, headers=headers)

        sleep(random.randint(1, 3))

        if response.status_code != 200:
            logger.warning('Error.')
            logger.warning(f'Status code: {response.status_code}')
            break

        sp = BeautifulSoup(response.content, 'html.parser')

        name = sp.find('h2', class_="title css-1k75zwy e1pl6npa11").text.strip()
        print(f'Getting name: {name}')

        genres_search = sp.find_all('span', class_='genre css-w9wtzg e1pl6npa8')

        genres = ''
        for g in genres_search:
            s = g.text.strip()
            genres += s + ', '

        genres = genres.rstrip(', ') if genres else None
        print(f'Getting genres: {genres}')

        rating = sp.find_all('svg', class_="star-icon css-1cftdwf e1pl6npa10")
        rating = len(rating) if rating else 0
        print(f'Getting rating: {rating}')

        description = sp.find('p', class_="description css-mkw8pm e1pl6npa0").text.strip()
        print(f'Getting description: {description}')

        dev = sp.find('span', class_="brand developer").text.strip()

        developer = dev.split(':')[1].strip()
        print(f'Getting developer: {developer}')

        game_platform = sp.find('span', class_="game-platforms-wrapper").text.strip()

        game_pl = game_platform.split(':')[1].strip()
        print(f'Getting game_pl: {game_pl}')

        multiplayer = sp.find(lambda tag: tag.name == 'span' and 'Type' in tag.text).text.strip()

        mp = multiplayer.split(':')[1].strip()
        print(f'Getting multiplayer: {mp}')

        price = sp.find('div', class_="price css-o7uf8d e1pl6npa6").text.strip()
        s = price.split(' ')[0]
        c = s.replace(',', '.')

        price_eur = float(c)

        print(f'Getting price_eur: {price_eur}')

        img = sp.find('div', class_="css-1qesdsb e1pl6npa2")
        img_url = 'https://sandbox.oxylabs.io' + img.find_all('img', class_='image')[1].get('src')

        print(f'Getting img_url: {img_url}')

        rn = random.randint(1, 3)

        sleep(rn)
        data = [
            name, genres, rating,
            description, game_pl,
            price_eur, mp,
            developer, img_url
        ]
        logger.info(f'Getting data: {data}')
        cards.append(data)
        p += 1

    return cards
