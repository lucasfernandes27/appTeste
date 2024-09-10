from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import pandas as pd
import time

driver = webdriver.Chrome()


driver.get("https://www.rpachallenge.com/")


download_button = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Download Excel')]"))
)
download_button.click()


excel_path = "/path/to/downloaded/file/challenge.xlsx"


data = pd.read_excel(excel_path)


start_button = driver.find_element(By.XPATH, "//button[contains(text(),'Start')]")
start_button.click()


for index, row in data.iterrows():
   
    form_fields = WebDriverWait(driver, 10).until(
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
            field.send_keys(form_mapping[label])

  
    submit_button = driver.find_element(By.XPATH, "//input[@type='submit']")
    submit_button.click()


    time.sleep(2)

driver.quit()
