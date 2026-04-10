import random
from time import sleep

from bs4 import BeautifulSoup
from selenium import webdriver

from scrap_games.settings import chrome_options, logger


def scrap_nintendo() -> tuple[str, str, int, str, str, float, str, str, str] | None:
    for n in range(1, 3001):
        URL = f'https://sandbox.oxylabs.io/products/{n}'
        logger.warning(f'Start parsing: {URL}')

        with webdriver.Chrome(options=chrome_options) as driver:
            driver.get(URL)
            content = driver.page_source

        sp = BeautifulSoup(content, 'html.parser')

        name = sp.find('h4', class_='title css-7u5e79 eag3qlw7').text.strip()
        print(f'Getting name: {name}')

        genres_search = sp.find_all('span', class_='genre css-w9wtzg e1pl6npa8')

        genres = ''
        for g in genres_search:
            s = g.text.strip()
            genres += s + ', '

        genres = genres.rstrip(', ')
        print(f'Getting genres: {genres}')

        rating = len(sp.find_all('svg', class_="star-icon css-1cftdwf e1pl6npa10"))
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

        img_url = 'https://sandbox.oxylabs.io' + sp.find('img', class_="image").get('src')
        print(f'Getting img_url: {img_url}')

        rn = random.randint(1, 3)

        sleep(rn)

        data = (name, genres, rating, description, game_pl, price_eur, mp, developer, img_url)
        print(data)
        logger.info(f'Getting data: {data}')
        return data
