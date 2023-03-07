# backend part
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
from fake_useragent import UserAgent
import random
import os
import gdown
from datetime import datetime
from file_exchange import gdrive_download, gdrive_upload, log_folder, gdrive_delete
import numpy as np
from math import pi

# dividing input file to parameters and urls list
def get_params(filename: str):
    file_data = []
    with open(f"/Users/admin/Desktop/LidEmulator/{filename}", "r") as urls:
        for url in urls:
            file_data.append(url.strip())
    params = list(map(int, file_data[0].split()))
    urls = file_data[1:]
    return params, urls


# downloading a config file from google drive link
def download_cfg(url: str):
    file_id = url.split('/')[-2]
    prefix = 'https://drive.google.com/uc?/export=download&id='
    gdown.download(prefix + file_id)


# user emulation for 1 url
class Emulation():
    def __init__(self, params, url):
        self.work_time = random.randint(params[0], params[1])
        self.percentage = params[2]
        self.repeatability = params[3]
        self.time_on_page = random.randint(params[4], params[5])
        self.transition_amount = random.randint(params[6], params[7])
        self.adv_transition = params[9]
        self.search_emulation = params[10]
        self.url = url
        self.scroll_time = (self.time_on_page * 60 - (15 if self.search_emulation else 0))/\
                           (self.transition_amount + 1 + (1 if self.adv_transition else 0))
        print(self.time_on_page)
        print(self.scroll_time)
        # creating webdriver
        # set options
        useragent = UserAgent().random
        options = Options()
        options.add_argument(f'user-agent={useragent}')
        # disabling webdriver mode
        options.add_argument("--disable-blink-features=AutomationControlled")
        self.driver = webdriver.Chrome(executable_path="/Users/admin/Desktop/LidEmulator/chromedriver/chromedriver",
                                       options=options)
        self.driver.maximize_window()

    def driver_get(self):
        self.driver.get(url=self.url)
        self.driver.maximize_window()

    # Imitation of user scrolling page
    def scroll(self):
        print('scrolling')
        time.sleep(1 + random.random())
        start_time = time.time()
        move_height = 0
        sign = 1
        doc_height = self.driver.execute_script("return document.documentElement.scrollHeight - document.documentElement.clientHeight")

        # scroll speed will be sinusoidal function
        step_amount = 30
        x = np.linspace(0, pi, step_amount)
        y = np.sin(x)

        # scroll imitation
        while time.time() - start_time < self.scroll_time:
            multiplier = random.randint(20, 60)
            for j in range(step_amount):
                move_height += round(multiplier * sign * y[j])
                self.driver.execute_script(f"window.scrollTo(0, {move_height});")
                time.sleep(random.random() / 20)
            if random.randint(1, 5) == 3:
                multiplier = random.randint(20, 60)
                time.sleep(1 + random.random())
                for k in range(step_amount):
                    move_height -= round(multiplier * sign * y[k])
                    self.driver.execute_script(f"window.scrollTo(0, {move_height});")
                    time.sleep(random.random() / 20)

            print(move_height)
            print(sign)
            # changing direction if page ended
            if move_height >= doc_height:
                move_height = doc_height
                sign *= -1
            if move_height < 0:
                move_height = 0
                sign *= -1

            sleep_time = random.randint(1, 15)
            # stop scrolling if time ran out
            if time.time() - start_time + sleep_time > self.scroll_time:
                sleep_ost = self.scroll_time - (time.time() - start_time)
                time.sleep(sleep_ost if sleep_ost > 0 else 0)
                break

            time.sleep(sleep_time + random.random())

    # imitation of user searching and follow a link
    def search(self):
        link = "https://www.bing.com/"
        self.driver.get(url=link)
        time.sleep(2 + random.random())
        input_str = self.driver.find_element(By.XPATH, '//input[@class="sb_form_q"]')
        input_str.clear()
        input_str.send_keys(self.url)
        time.sleep(2 + random.random())

        actions = ActionChains(self.driver)
        actions.send_keys(Keys.ENTER)
        actions.perform()
        time.sleep(2 + random.random())

        first_link = self.driver.find_element(By.XPATH, '//a[@class="sh_favicon"]').get_attribute('href')
        self.driver.get(url=first_link)

    # imitation of user following advertising link
    def adv(self):
        print('Reklama')
        elements = self.driver.find_elements(By.XPATH, './/*')
        for element in elements:
            print('loading...')
            try:
                if str(element.text.lower().strip()) == 'реклама':
                    print(element.text)
                    element.click()
                    time.sleep(1)
                    break
            except Exception as ex:
                print(ex)

    # Imitation of user following random link on current website
    def transition(self):
        action_chain = ActionChains(self.driver)
        links = self.driver.find_elements(By.PARTIAL_LINK_TEXT, '')
        link_flag = True

        while link_flag:
            link = links.pop(random.randint(0, len(links)-1))
            try:
                print(f'пробуем: {link.get_attribute("href")}')
                if link.get_attribute('href').find('https') < 0:
                    a = 1/0
                action_chain.move_to_element(link).perform()
                link.click()
                link_flag = False
                print('Эта оказалась норм')
            except:
                if len(links) == 1:
                    link_flag = False
                print(f"Transition problem {len(links)}")

    # Function that creates sequence of all actions on one website
    def emulation(self):
        emulation_functions = []
        if self.search_emulation:
            emulation_functions.append(self.search)
            emulation_functions.append(self.scroll)
        else:
            emulation_functions.append(self.driver_get)
            emulation_functions.append(self.scroll)

        if self.adv_transition:
            emulation_functions.append(self.adv)
            emulation_functions.append(self.scroll)
        for i in range(self.transition_amount):
            emulation_functions.append(self.transition)
            emulation_functions.append(self.scroll)
        return emulation_functions

    # Function that performs all the actions added to the sequence
    def perform(self):
        funcs = self.emulation()
        try:
            for func in funcs:
                func()
        except Exception as ex:
            print(ex)
        finally:
            self.driver.close()
            self.driver.quit()

#__________________________________________________________________________________________
# Main cycle that performs emulations for all urls and uploads new info
class MainCycle():
    def __init__(self, robot_id):
        self.params, self.old_urls = get_params(f'config_{robot_id}.txt')
        self.updated_params = self.params
        self.updated_urls = self.old_urls
        self.work_time = (self.params[0], self.params[1])
        self.percentage = self.params[2]
        self.repeatability = self.params[3]
        self.robot_id = self.params[8]
        self.reload_flag = False

    # creating urls array based on urls, percentage and repeatability parameters
    def new_urls(self):
        new_len_array = round(len(self.old_urls) * self.percentage / 100)
        self.new_urls_array = self.old_urls[:new_len_array] * (self.repeatability + 1)
        random.shuffle(self.new_urls_array)
        print(new_len_array)
        print(self.new_urls_array)
        return self.new_urls_array

    # writing log for autostart in case of reboot
    def log(self):
        log_string = f"Robot ID {self.robot_id} - успешно запущен\n"
        log_title = f'log_{self.robot_id}.txt'
        gdrive_upload(log_title, log_string, log_folder)
        with open('log.txt', 'w') as file:
            file.write(log_string)

    def delete_used_files(self):
        log_title = f'log_{self.robot_id}.txt'
        gdrive_delete(log_title, log_folder)
        os.remove('log.txt')
        os.remove(f'config_{self.robot_id}.txt')

    def go_to_sleep(self):
        current_hour, current_minute = map(int, datetime.today().strftime('%H %M').split())
        if current_hour >= self.work_time[1] or current_hour <= self.work_time[0]:
            if current_hour >= self.work_time[1]:
                rest_time = (24 - current_hour - 1 + self.work_time[0]) * 3600 + (60 - current_minute) * 60
                print(f'Rest time is {rest_time}')
                time.sleep(rest_time)
            if current_hour < self.work_time[0]:
                rest_time = (self.work_time[0] - current_hour - 1) * 3600 + (60 - current_minute) * 60
                print(f'Rest time is {rest_time}')
                time.sleep(rest_time)
            gdrive_download(f'config_{self.robot_id}.txt')
            self.updated_params, self.updated_urls = get_params(f'config_{self.robot_id}.txt')
            if self.updated_params != self.params or self.updated_urls != self.old_urls:
                self.old_urls = self.updated_urls
                self.params = self.updated_params
                self.reload_flag = True
                return True
        return False

    # main working cycle
    def main(self):
        self.log()
        urls = self.new_urls()
        for url in urls:
            # function freezes program if working day ended and checks file changes after awake
            file_updated = self.go_to_sleep()
            if file_updated:
                break
            emulation = Emulation(self.params, url)
            emulation.perform()

        self.delete_used_files()

        if self.reload_flag:
            self.main()



if __name__ == "__main__":
    main_cycle = MainCycle('777')
    main_cycle.main()
