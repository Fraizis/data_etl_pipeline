from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

options = Options()
options.add_argument("--headless")  # Тот самый headless режим. Можно использовать "--headless=new"
options.add_argument("--disable-gpu")  # Отключаем GPU для стабильности
options.add_argument("--no-sandbox")  # Нужно для Linux
options.add_argument("--window-size=1920,1080")  # Размер окна

# driver = webdriver.Chrome(options=options)

url = 'https://sandbox.oxylabs.io/products/1'


driver = webdriver.Chrome(options=options)
driver.get(url)
content = driver.page_source

# with webdriver.Chrome(options=chrome_options) as driver:
#     driver.get(url)
#     content = driver.page_source

# write the page content
# with open('page.html', 'w') as fp:
#     fp.write(content)

rating = driver.find_elements(By.CSS_SELECTOR, 'svg.star-icon.css-1cftdwf.e1pl6npa10')
print(len(rating))
# element = driver.find_element(By.CLASS_NAME, "css-1k75zwy")
# element = driver.find_element(By.XPATH, "//div[@class='title css-1k75zwy e1pl6npa11']")
# title css-1k75zwy e1pl6npa11
#
print()

driver.close()
