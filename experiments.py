from math import sin, pi
import matplotlib.pyplot as plt
import numpy as np
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time


url = 'https://povar.ru/'
driver = webdriver.Chrome(executable_path="/Users/admin/Desktop/LidEmulator/chromedriver/chromedriver")
driver.maximize_window()
driver.get(url=url)



def benchmark(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        func(*args, **kwargs)
        print(time.time() - start)

    return wrapper

@benchmark
def perform(driver):
    elements = driver.find_elements(By.XPATH, './/*')
    for element in elements:
        print('loading...')
        try:
            adv = str(element.text.lower().strip())

            if adv == 'реклама':
                print(element.text)
                element.click()
                break
        except Exception as ex:
            print(ex)

perform(driver)