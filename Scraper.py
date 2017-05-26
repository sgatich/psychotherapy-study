from selenium import webdriver
from os.path import expanduser
from selenium.common.exceptions import TimeoutException, WebDriverException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time

apsaa_link = "http://www.apsa.org/find-an-analyst"
delay = 10

class Scraper:
    def run(self):
        pass


class ApsaaScraper(Scraper):
    def __init__(self):
        self.set_chrome()
        states_file = open("states.txt", "r")
        self.states_list = states_file.readlines()
        self.analysts_info_list = []

    def set_phantom(self):
        home = expanduser("~")
        self.phantomBrowser = webdriver.PhantomJS(home + "/phantomjs/bin/phantomjs")

    def set_chrome(self):
        home = expanduser("~")
        self.phantomBrowser = webdriver.Chrome(home + "/chromedriver")

    def run(self):
        for state in self.states_list:
            self.phantomBrowser.get(apsaa_link)
            self.analysts_info_list.append("######################State: " + state)
            self.analysts_info_list.append("\n\n\n")
            self.obtain_analysts_for_state(state)
            self.analysts_info_list.append("\n\n\n")

        analysts_file = open("APSAA-analysts", "w")
        analysts_file.writelines(self.analysts_info_list)
        analysts_file.close()

    def obtain_analysts_for_state(self, state):
        try:
            WebDriverWait(self.phantomBrowser, delay).until(
                EC.presence_of_element_located((By.ID, "edit-user-state"))
            )
            print("Page is loaded!")
        except TimeoutException:
            print("Loading took too much time!")

        state_input = self.phantomBrowser.find_element_by_css_selector("input#edit-user-state")
        state_input.send_keys(state)

        time.sleep(10)

        # submit_button = self.phantomBrowser.find_element_by_css_selector("input#edit-submit")
        # submit_button.click()
        #
        # try:
        #     WebDriverWait(self.phantomBrowser, delay).until(
        #         EC.presence_of_element_located((By.ID, "page-title"))
        #     )
        #     print("Page is ready!")
        # except TimeoutException:
        #     print("Loading took too much time!")
        #
        try:
            analysts_results = self.phantomBrowser.find_elements_by_css_selector("div.analyst_result_unit")
        except WebDriverException:
            print("An error occured.")

        print(len(analysts_results))
        #
        #
        # print("Analysts: ")
        for analyst_result in analysts_results:
            self.analysts_info_list.append(analyst_result.text)
            self.analysts_info_list.append("\n")
            print(analyst_result.text)
        #
        # self.phantomBrowser.back()
