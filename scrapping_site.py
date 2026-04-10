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

# with open('output.txt', 'w') as f:
#     print(soup.prettify(), file = f)


# url1 = 'https://sandbox.oxylabs.io/products/1'

# response = requests.get(url1, headers=headers)

#
# soup = BeautifulSoup(response.content, 'html.parser')
# print(soup.prettify())

# with open('output.txt', 'w') as f:
#     print(soup.prettify(), file = f)

# data = []

# cards = soup.find_all('a')
# print(cards)

# for i in cards:
#     print(i.get('href'))

# script_tag = sp.find('script', {"id": "__NEXT_DATA__", "type": "application/json"})

# if script_tag is not None:
#     # Извлекаем содержимое тега
#     json_data = json.loads(script_tag.get_text())

# name = sp.find('h4', class_='title css-7u5e79 eag3qlw7').text.strip()
# print(name)
