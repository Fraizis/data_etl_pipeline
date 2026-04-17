import random
from time import sleep
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from scrap_games.settings import URL, logger

options = Options()
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
options.add_argument("--window-size=1920,1080")


def scrap_card():
    p = 2999
    cards = []

    while True:
        user_agent = UserAgent().random
        logger.info(f'User-Agent used: {user_agent}')

        url = f'{URL}{p}'

        headers = {'User-Agent': user_agent}

        logger.info(f'Start parsing: {url}')

        response = requests.get(url, headers=headers)

        sleep(random.randint(1, 3))

        if response.status_code != 200:
            logger.warning('Error.')
            logger.warning(f'Status code: {response.status_code}')
            break

        options.add_argument(f"user-agent={user_agent}")

        driver = webdriver.Chrome(options=options)
        driver.get(url)

        content = driver.page_source

        sp = BeautifulSoup(content, 'html.parser')

        name = sp.find('h2', class_="title css-1k75zwy e1pl6npa11").text.strip()

        genres_search = sp.find_all('span', class_='genre css-w9wtzg e1pl6npa8')

        genres = ''
        for g in genres_search:
            s = g.text.strip()
            genres += s + ', '

        genres = genres.rstrip(', ') if genres else None

        rating = sp.find_all('svg', class_="star-icon css-1cftdwf e1pl6npa10")
        rating = len(rating) if rating else 0

        description = sp.find('p', class_="description css-mkw8pm e1pl6npa0").text.strip()

        dev = sp.find('span', class_="brand developer").text.strip()

        developer = dev.split(':')[1].strip()

        game_platform = sp.find('span', class_="game-platforms-wrapper").text.strip()

        game_pl = game_platform.split(':')[1].strip()

        multiplayer = sp.find(lambda tag: tag.name == 'span' and 'Type' in tag.text).text.strip()

        mp = multiplayer.split(':')[1].strip()

        price = sp.find('div', class_="price css-o7uf8d e1pl6npa6").text.strip()
        s = price.split(' ')[0]
        c = s.replace(',', '.')

        price_eur = float(c)

        img = sp.find('div', class_="css-1qesdsb e1pl6npa2")
        img_url = 'https://sandbox.oxylabs.io' + img.find_all('img', class_='image')[1].get('src')

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

        driver.quit()

        sleep(random.randint(1, 3))

    return cards
