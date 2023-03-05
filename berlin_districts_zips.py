from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
import pandas as pd
import time

PATH = '../usr/local/bin/chromedriver'
SERVICE = webdriver.chrome.service.Service(executable_path=PATH)
WEBSITE = "https://www.in-berlin-brandenburg.com/Berliner_Bezirke/plz-berlin.html"

driver = webdriver.Chrome(service=SERVICE)

driver.get(WEBSITE)
time.sleep(10)

all_objects = driver.find_elements(By.XPATH, "//h4")
all_grids = driver.find_elements(By.XPATH, "//div[@class='grid']")

i = 0

rows_list = []

for district in all_objects:
    zips = all_grids[i].find_elements(By.TAG_NAME, "li")

    for zip_code in zips:
        dict_1 = {}
        dict_1.update([('district', district.text), ('ZIP', zip_code.text)])
        rows_list.append(dict_1)

    i += 1

df = pd.DataFrame(rows_list)
df.drop(df[df['ZIP'] == '-'].index, inplace=True)

df = df.reset_index()

split_strings = ['Ortsteil ', 'Postleitzahl ', 'PLZ Berlin ', 'Berlin']

for string in split_strings:
    for index, row in df.iterrows():
        if string in row['district']:
            df.loc[index, 'district'] = row['district'].split(string)[1]

df.to_csv('berlin_districts_zips.csv')
