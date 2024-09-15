import os
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(options=chrome_options)

driver.get("https://www.rpachallenge.com/")

time.sleep(5)  

download_folder = os.path.expanduser("~/Downloads")
excel_file_name = "challenge.xlsx"  
excel_path = os.path.join(download_folder, excel_file_name)

if not os.path.exists(excel_path):
    print(f"Arquivo {excel_file_name} não encontrado em {download_folder}.")
    driver.quit()
else:
    print(f"Usando o arquivo {excel_file_name} localizado em {download_folder}.")

data = pd.read_excel(excel_path)

try:
    start_button = WebDriverWait(driver, 30).until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Start')]"))
    )
    start_button.click()

    for index, row in data.iterrows():
        form_fields = WebDriverWait(driver, 30).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "input[type='text']"))
        )

       
        form_mapping = {
            "First Name": row['First Name'],
            "Last Name": row['Last Name'],
            "Company Name": row['Company Name'],
            "Role in Company": row['Role in Company'],
            "Address": row['Address'],
            "Email": row['Email'],
            "Phone Number": row['Phone Number']
        }

        for field in form_fields:
            label = field.get_attribute('aria-label') 
            if label in form_mapping:
                field.clear()
                field.send_keys(form_mapping[label])

        
        submit_button = driver.find_element(By.XPATH, "//input[@type='submit']")
        submit_button.click()

  
        time.sleep(2)

except TimeoutException as e:
    print(f"Erro de timeout ao localizar um elemento: {str(e)}")
finally:
    driver.quit()
