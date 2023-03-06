# backend part
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
import time
from fake_useragent import UserAgent
import random
import pickle
import requests

# def all_page_links(url: str):
#     links = []
#     soup = BeautifulSoup(requests.get(url).text, 'lxml')
#     for link in soup.find_all('a'):
#         link_txt = link.get_text('href')
#         if len(link_txt.strip()) > 1:
#             links.append(link_txt.strip())
#     return links

def random_link_clicks(driver):

    action_chain = ActionChains(driver)
    links = driver.find_elements(By.PARTIAL_LINK_TEXT, '')
    link = links.pop(random.randint(0, len(links)))

    try:
        action_chain.move_to_element(link).perform()
        time.sleep(3)
        link.click()
    except:
        print("Problem with transition")

def get_url_list(filename: str):
    url_list = []
    with open(f"/Users/admin/Desktop/LidEmulator/{filename}", "r") as urls:
        for url in urls:
            url_list.append(url.strip())
    return url_list[1:]

def random_scroll(driver):
    time.sleep(3+random.random())
    move_height = 0
    sign = 1
    doc_height = driver.execute_script("return document.documentElement.scrollHeight - document.documentElement.clientHeight")
    for i in range(random.randint(5,10)):
        for j in range(random.randint(20, 100)):
            move_height += random.randint(5, 10) * sign
            driver.execute_script(f"window.scrollTo(0, {move_height});")
            time.sleep(random.random() / 40)
        if random.randint(1, 5) == 3:
            time.sleep(random.randint(1, 3) + random.random())
            for k in range(random.randint(10, 50)):
                move_height -= random.randint(5, 10) * sign
                driver.execute_script(f"window.scrollTo(0, {move_height});")
                time.sleep(random.random() / 40)
        if move_height >= doc_height:
            move_height = doc_height
            sign *= -1
        if move_height < 0:
            move_height = 0
            sign *= -1
        print(doc_height)
        print(move_height)
        print(sign)
        time.sleep(random.randint(1, 15)+random.random())

def yandex(driver, url):
    link = "https://www.yahoo.com/"
    driver.get(url=link)
    time.sleep(2+random.random())
    input_str = driver.find_element(By.XPATH, '//input[@class="_yb_i33se"]')
    input_str.clear()
    input_str.send_keys(url)
    time.sleep(2+random.random())

    actions = ActionChains(driver)
    actions.send_keys(Keys.ENTER)
    actions.perform()
    time.sleep(2+random.random())

    first_link = driver.find_element(By.XPATH, '//a[@class=" d-ib fz-20 lh-26 td-hu tc va-bot mxw-100p"]').get_attribute('href')
    driver.get(url=first_link)

def movement(url: str):
    # creating fake user agent

    useragent = UserAgent().random
    # set options
    options = Options()
    options.add_argument(f'user-agent={useragent}')
    # disabling webdriver mode
    #options.add_argument("--disable-blink-features=AutomationControlled")
    driver = webdriver.Chrome(executable_path="/Users/admin/Desktop/LidEmulator/chromedriver/chromedriver",
                              options=options)
    # driver.maximize_window()

    try:
        # driver.get(url=url)
        # time.sleep(30)
        # for cookie in pickle.load(open("cookies", "rb")):
        #     driver.add_cookie(cookie)
        #
        # driver.refresh()
        # time.sleep(2)

        time.sleep(1)
        # if random.randint(1,3) == 1:
        yandex(driver, url)
        # else:
        #     driver.get(url=url)
        random_scroll(driver)
        random_link_clicks(driver)
        random_scroll(driver)
        time.sleep(2)
    except Exception as ex:
        print(ex)
    finally:
        driver.close()
        driver.quit()

def main():
    url_list = get_url_list('url_111.txt')
    for url in url_list:
        movement(url)
        time.sleep(2)


if __name__ == "__main__":
    main()