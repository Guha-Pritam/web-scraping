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


# Disables
logging.getLogger('WDM').setLevel(logging.NOTSET)
os.environ['WDM_LOG'] = "false"


class FindChips(object):
    def __init__(self):
        self.CATEGORY = []
        self.SUBCATEGORY = []
        self.options = Options()
        # Headless Mode
        self.options.add_argument("--window-size=1920,1080")
        self.options.add_argument("--headless")
        self.options.add_argument("--disable-gpu")
        self.options.add_argument(
            "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"
        )
        # ------------
        self.options.add_argument("start-maximized")
        # options.add_argument('window-size=1920x1080')
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
        # self.driver.get("http://www.findchips.com/parametric")

    def get_category_list(self):
        print("[ info ] Querying available categories from findchips website")
        self.driver.get("http://www.findchips.com/parametric")
        XPATH_ELEMENT_CATEGORY = '//*[@id="page"]/ul'
        self.wait.until(EC.presence_of_element_located((By.XPATH, XPATH_ELEMENT_CATEGORY)))
        category_list = self.driver.find_element(By.XPATH, XPATH_ELEMENT_CATEGORY)
        self.driver.execute_script("arguments[0].scrollIntoView();", category_list)
        self.CATEGORY = []
        for num, i in enumerate(category_list.find_elements(By.TAG_NAME, 'li')):
            self.CATEGORY.append(i.text.split("\n")[0])
            # print(f'[ {str(num + 1).zfill(2)} ] ', self.CATEGORY[num])
        return self.CATEGORY

    def open_category(self, category):
        cat_button = self.driver.find_element(By.PARTIAL_LINK_TEXT, category)
        self.driver.execute_script("arguments[0].click();", cat_button)

    def get_subcategory_list(self):
        print("[ info ] Querying available sub-categories from findchips website")
        XPATH_SUBCATEGORY = '//*[@id="page"]/ul'
        self.wait.until(EC.presence_of_element_located((By.XPATH, XPATH_SUBCATEGORY)))
        subcategory_list = self.driver.find_element(By.XPATH, XPATH_SUBCATEGORY)
        self.SUBCATEGORY = []
        for num, i in enumerate(subcategory_list.find_elements(By.TAG_NAME, 'li')):
            self.SUBCATEGORY.append(i.text.split("\n")[0])
            # print(f"[ {str(num + 1).zfill(2)} ] {self.SUBCATEGORY[num]}")
        return self.SUBCATEGORY

    def open_subcategory(self, subcategory):
        sub_cat_button = self.driver.find_element(By.PARTIAL_LINK_TEXT, subcategory)
        self.driver.execute_script("arguments[0].click();", sub_cat_button)

    def store_data_in_csv(self, filename, total_number_of_data):
        self.wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="j-parametric-table-header"]/thead/tr[2]')))
        # print([self.driver.find_element(By.CLASS_NAME, 'para-filters-info').text])
        HEADER = []
        for i in self.driver.find_element(By.XPATH, '//*[@id="j-parametric-table-header"]/thead/tr[2]').find_elements(
                By.TAG_NAME, "th"):
            HEADER.append(str(i.text))
        count = 0
        file_handler = open(filename, "w+", encoding="utf-8", newline="")
        csv_write = csv.writer(file_handler)
        csv_write.writerow(HEADER)
        while 1:
            self.wait.until(EC.presence_of_element_located((By.ID, 'j-parametric-table')))
            for i in self.driver.find_element(By.ID, 'j-parametric-table').find_elements(By.TAG_NAME, "tr"):
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
                self.driver.find_element(By.CLASS_NAME, 'paginator-next').click()
            except NoSuchElementException as excp:
                file_handler.close()
                print("[ info ] data querying completed")
                print(f"[ info ] data stored in {filename}")
                return

    def __del__(self):
        if self.driver:
            self.driver.close()
        counter = 10
        for ind in range(counter, 0, -1):
            print(f"\r[ info ] program will close in {str(ind).zfill(2)}", end="")
            time.sleep(1)
        print("")
        # self.__terminat_program()


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
        subcategory = obj.get_subcategory_list()
        num = 0
        for num, i in enumerate(subcategory):
            print(f"[{str(num + 1).zfill(2)}] {i}")
        while 1:
            user_sub_cat = input("Select any subcategory :")
            if not user_sub_cat.isdigit() or not 1 <= int(user_sub_cat) <= len(obj.SUBCATEGORY):
                print(f"[ info ] Invalid Input please enter value between 1 - {len(obj.SUBCATEGORY)}")
            else:
                break
        user_sub_cat = int(user_sub_cat) - 1
        obj.open_subcategory(obj.SUBCATEGORY[user_sub_cat])
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
