from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from time import sleep
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
import pickle

url = 'https://ya.ru/'
url_request = f'https://yandex.ru/search/?text={url}&lr=213'
options = Options()
options.add_argument("--disable-blink-features=AutomationControlled")
driver = webdriver.Chrome(executable_path="/Users/admin/Desktop/LidEmulator/chromedriver/chromedriver",
                              options=options)
driver.maximize_window()


driver.get(url=url_request)
sleep(10)
for cookie in pickle.load(open("cookies", "rb")):
    driver.add_cookie(cookie)
driver.refresh()
sleep(10)
