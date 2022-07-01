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

options = Options()
# Headless Mode
options.add_argument("--window-size=1920,1080")
# options.add_argument("--headless")
options.add_argument("--disable-gpu")
# options.add_argument(
#     "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"
# )
# ------------
options.add_argument("start-maximized")
# options.add_argument('window-size=1920x1080')
options.add_argument('--no-sandbox')
options.add_experimental_option("useAutomationExtension", False)
options.add_experimental_option("excludeSwitches", ["enable-automation"])
try:
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    print("[ info ] Created chrome driver")

except Exception as excp:
    driver = None
    print("[ info ] Failed to created chrome instance please install chrome and try again")
    sys.exit()

wait = WebDriverWait(driver, 60)
driver.get('https://www.digikey.in/en/products')
product_xpath = '//*[@id="__next"]/main/div/div/div[2]/div[1]/section/div/div[4]/div[2]/div/ul'
wait.until(EC.presence_of_all_elements_located((By.XPATH, product_xpath)))
products = driver.find_element(By.XPATH, product_xpath)
# driver.execute_script("arguments[0].scrollIntoView();", products)

for ele in products.find_elements(By.TAG_NAME, "li"):
    # driver.execute_script("arguments[0].scrollIntoView(true);", ele)
    print(ele.text)
