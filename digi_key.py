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


class DigiKey(object):
    def __init__(self):
        self.PRODUCTS = []
        self.SUB_PRODUCTS = []
        self.options = Options()
        # Headless Mode
        self.options.add_argument("--window-size=1920,1080")
        self.options.add_argument("--headless")
        self.options.add_argument("--disable-gpu")
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

        self.wait = WebDriverWait(self.driver, 80)

    def get_product_list(self):
        print("[ info ] Querying available categories from digi_key website")
        self.driver.get("https://www.digikey.in/en/products")
        XPATH_ELEMENT_PRODUCTS = '//*[@id="__next"]/main/div/div/div[2]/div[1]/section/div/div[4]/div[2]/div/ul'
        self.wait.until(EC.presence_of_element_located((By.XPATH, XPATH_ELEMENT_PRODUCTS)))
        product_list = self.driver.find_element(By.XPATH, XPATH_ELEMENT_PRODUCTS)
        self.PRODUCTS = []
        print(self.PRODUCTS)
        for num, i in enumerate(product_list.find_elements(By.TAG_NAME, "li")):
            self.PRODUCTS.append(i.text.split("\n")[0])
            # print(i.text)
        return self.PRODUCTS

    def open_product_list(self, category):
        cat_button = self.driver.find_element(By.PARTIAL_LINK_TEXT, category)
        self.driver.execute_script("arguments[0].click();", cat_button)

    def sub_products_list(self):
        print("[ info ] Querying available sub-categories from digi_key website")
        XPATH_SUB_PRODUCT = '//*[@id="__next"]/main/div/div/div[1]/div[1]/section/div/div[4]/div[2]/ul'
        self.wait.until(EC.presence_of_element_located((By.XPATH, XPATH_SUB_PRODUCT)))
        sub_products_list = self.driver.find_element(By.XPATH, XPATH_SUB_PRODUCT)
        self.SUB_PRODUCTS = []
        for num, i in enumerate(sub_products_list.find_elements(By.TAG_NAME, 'li')):
            self.SUB_PRODUCTS.append(i.text.split("\n")[0])
        return self.SUB_PRODUCTS

    def open_sub_products(self, open_sub_products):
        sub_cat_button = self.driver.find_element(By.PARTIAL_LINK_TEXT, open_sub_products)
        self.driver.execute_script("arguments[0].click();", sub_cat_button)

    def store_data_in_csv(self, filename, total_number_of_data):
        self.wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="data-table-0"]/thead/tr[2]')))
        HEADER = []
        for i in self.driver.find_element(By.XPATH, '//*[@id="data-table-0"]/thead/tr[2]').find_elements(
                By.TAG_NAME, "th"):
            HEADER.append(str(i.text))
        count = 0
        file_handler = open(filename, "w+", encoding="utf-8", newline="")
        csv_write = csv.writer(file_handler)
        csv_write.writerow(HEADER)
        while 1:
            self.wait.until(EC.presence_of_element_located((By.ID, 'data-table-0')))
            for i in self.driver.find_element(By.ID, 'data-table-0').find_elements(By.TAG_NAME, "tr"):
                if not total_number_of_data == -1 and count >= total_number_of_data:
                    file_handler.close()
                    print("[ info ] data querying completed")
                    print(f"[ info ] data stored in {filename}")
                    return
                temp = []
                for j in i.find_elements(By.TAG_NAME, "td"):
                    temp.append(str(j.text))
                count += 1
                print(f"[{str(count).zfill(4)}] ", temp)
                csv_write.writerow(temp)
            try:
                self.driver.find_element(By.CLASS_NAME, 'MuiButtonBase-root MuiIconButton-root jss321 jss727').click()
            except NoSuchElementException as excp:
                file_handler.close()
                print("[ info ] data querying completed")
                print(f"[ info ] data stored in {filename}")
                return


def main():
    obj = DigiKey()
    while 1:
        product = obj.get_product_list()
        num = 0
        for num, i in enumerate(product):
            print(f"[{str(num + 1).zfill(2)}] {i}")
        print(f"[{str(num + 2).zfill(2)}] Exit")
        while 1:
            user_cat = input("Select any products :")
            if not user_cat.isdigit() or not 1 <= int(user_cat) <= len(obj.PRODUCTS) + 1:
                print(f"[ info ] Invalid Input please enter value between 1 - {len(obj.PRODUCTS) + 1}")
            else:
                user_cat = int(user_cat) - 1
                break
        if user_cat == num + 1:
            sys.exit()

        obj.open_product_list(obj.PRODUCTS[user_cat])
        sub_products = obj.sub_products_list()
        num = 0
        for num, i in enumerate(sub_products):
            print(f"[{str(num + 1).zfill(2)}] {i}")
        while 1:
            user_sub_cat = input("Select any sub_products :")
            if not user_sub_cat.isdigit() or not 1 <= int(user_sub_cat) <= len(obj.SUB_PRODUCTS):
                print(f"[ info ] Invalid Input please enter value between 1 - {len(obj.SUB_PRODUCTS)}")
            else:
                break
        user_sub_cat = int(user_sub_cat) - 1
        obj.open_sub_products(obj.SUB_PRODUCTS[user_sub_cat])
        while 1:
            file_name = input("Enter file name to store the data :")
            if not file_name.endswith(".csv"):
                print("[ info ] Invalid input please enter filename ends with .csv")
            else:
                break
        while 1:
            total_data = input("Enter total number of data to collect [-1 to collect all data] :")
            try:
                total_data = int(total_data)
                break
            except ValueError:
                print("[ info ] Invalid input please enter input in digits")

        obj.store_data_in_csv(file_name, total_data)


if __name__ == "__main__":
    main()
