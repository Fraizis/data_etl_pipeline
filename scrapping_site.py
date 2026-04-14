from time import sleep

import requests
from bs4 import BeautifulSoup

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/145.0.0.0 Safari/537.36 OPR/129.0.0.0'
}

url = 'https://sandbox.oxylabs.io/products'
response = requests.get(url, headers=HEADERS)

soup = BeautifulSoup(response.content, 'html.parser')
# print(soup.prettify())

# Найти первый абзац:

first_paragraph = soup.find('p')

# Найти все абзацы:

all_paragraphs = soup.find_all('p')

# Один элемент с классом 'content':

content = soup.find(class_='content')

# Все элементы с классом 'content':

all_content = soup.find_all(class_='content')

# Поиск ссылки по href:

link = soup.find('a', href='https://example.com')

# Поиск по нескольким атрибутам

element = soup.find('div', attrs={'id': 'main', 'class': 'content'})

# Найти все абзацы с определенным классом:

paragraphs = soup.find_all('p', class_='text-block')

# Найти все ссылки внутри div с определенным id:

links = soup.find('div', id='menu').find_all('a')
