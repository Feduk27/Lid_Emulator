import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import time
from selenium.webdriver.common.by import By

url = 'https://wkusno-polesno.ru/'

driver = webdriver.Chrome(executable_path="/Users/admin/Desktop/LidEmulator/chromedriver/chromedriver")
driver.get(url=url)
driver.maximize_window()

elements = driver.find_elements(By.XPATH, './/*')
for element in elements:
    print('loading...')
    try:
        if str(element.text.lower().strip()) == 'реклама':

            element.click()


    except Exception as ex:
        print(ex)


# soup = BeautifulSoup(driver.page_source, 'lxml')
# links = soup.find_all()
# for link in links:
#     if link.get_text().strip().lower() == 'реклама':
#         soupik = BeautifulSoup(str(link), 'lxml')
#         soupik.find_all()
#         for s in soupik:
#             print(s)







