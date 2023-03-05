from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
import pandas as pd
import time

PATH = '../usr/local/bin/chromedriver'
SERVICE = webdriver.chrome.service.Service(executable_path=PATH)
WEBSITE = "https://www.in-berlin-brandenburg.com/Berliner_Bezirke/Ortsteile.html"

driver = webdriver.Chrome(service=SERVICE)

driver.get(WEBSITE)
time.sleep(7)

all_objects = driver.find_elements(By.XPATH, "//p/a/strong")
all_grids = driver.find_elements(By.XPATH, "//div[@class='grid']")

i = 0

rows_list = []

for grid in all_grids:
    ortsteile = grid.find_elements(By.TAG_NAME, "a")
    bezirk = all_objects[i].text

    for OT in ortsteile:
        ortsteil = OT.text
        dict_1 = {}
        dict_1.update([('sub_district', ortsteil), ('district', bezirk)])
        rows_list.append(dict_1)

    i += 1

df = pd.DataFrame(rows_list)
df.drop(df[df['sub_district'] == '-'].index, inplace=True)

df['district'] = df['district'].apply(lambda x: str(x).split(':')[0])

for index, row in df.iterrows():
    if 'Ortsteil ' in row['sub_district']:
        df.loc[index, 'sub_district'] = row['sub_district'].split('Ortsteil ')[1]

df.to_csv('berlin_districts_sub-districts.csv')
