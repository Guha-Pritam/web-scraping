import os
import csv
import sys
import time
import logging

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC


class FindChips(object):
    def __init__(self):
        self.CATEGORY = []
        self.SUBCATEGORY = []
        self.options = Options()
        # Headless Mode
        self.options.add_argument("--window-size=1920,1080")
        # self.options.add_argument("--headless")
        self.options.add_argument("--disable-gpu")
        self.options.add_argument(
            "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"
        )
        # ------------
        self.options.add_argument("start-maximized")
        self.options.add_argument('--no-sandbox')
        self.options.add_experimental_option("useAutomationExtension", False)
        self.options.add_experimental_option("excludeSwitches", ["enable-automation"])
        try:
            self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=self.options)
            print("[ info ] Created chrome driver")

        except Exception as excp:
            self.driver = None
            print("[ info ] Failed to created chrome instance please install chrome and try again")
            sys.exit()

        self.wait = WebDriverWait(self.driver, 60)

    def get_category_list(self):
        print("[ info ] Querying available categories from findchips website")
        self.driver.get("https://www.avnet.com/shop/AllProducts")
        XPATH_ELEMENT_CATEGORY = '//*[@id="content"]/section/div/div[1]'
        self.wait.until(EC.presence_of_element_located((By.XPATH, XPATH_ELEMENT_CATEGORY)))
        category_list = self.driver.find_element(By.XPATH, XPATH_ELEMENT_CATEGORY)
        self.driver.execute_script("arguments[0].scrollIntoView();", category_list)
        self.CATEGORY = []
        for num, i in enumerate(category_list.find_elements(By.TAG_NAME, 'div')):
            self.CATEGORY.append(i.text.split("\n")[0])
            # print(f'[ {str(num + 1).zfill(2)} ] ', self.CATEGORY[num])
        return self.CATEGORY

    def open_category(self, category):
        cat_button = self.driver.find_element(By.PARTIAL_LINK_TEXT, category)
        self.driver.execute_script("arguments[0].click();", cat_button)


def main():
    obj = FindChips()
    while 1:
        category = obj.get_category_list()
        num = 0
        for num, i in enumerate(category):
            print(f"[{str(num + 1).zfill(2)}] {i}")
        print(f"[{str(num + 2).zfill(2)}] Exit")
        while 1:
            user_cat = input("Select any category :")
            if not user_cat.isdigit() or not 1 <= int(user_cat) <= len(obj.CATEGORY) + 1:
                print(f"[ info ] Invalid Input please enter value between 1 - {len(obj.CATEGORY) + 1}")
            else:
                user_cat = int(user_cat) - 1
                break
        if user_cat == num + 1:
            sys.exit()

        obj.open_category(obj.CATEGORY[user_cat])


if __name__ == "__main__":
    main()
