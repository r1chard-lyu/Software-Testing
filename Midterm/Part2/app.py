from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from time import sleep

from selenium.webdriver.chrome.options import Options
options = Options()
options.add_argument('--headless')
options.add_argument('--window-size=1920,1080')
options.add_argument('--disable-gpu')
driver_path = ChromeDriverManager().install()
driver = webdriver.Chrome(executable_path=driver_path, options=options)



#Q2-1
print(f"[*] Go to https://docs.python.org/3/tutorial/index.html.")
driver.get("https://docs.python.org/3/tutorial/index.html")


language_dropdown = driver.find_element(By.CSS_SELECTOR, "select#language_select")
driver.execute_script("arguments[0].value = 'zh-tw'; arguments[0].dispatchEvent(new Event('change'));", language_dropdown)



# Wait for page to load and language to change
sleep(10)


print(f"[*] Print the title and first paragraph\n")
# Get title and description
title_element = driver.find_element(By.CSS_SELECTOR, "meta[property='og:title']")
description_element = driver.find_element(By.CSS_SELECTOR, "meta[property='og:description']")
title = title_element.get_attribute("content")
description = description_element.get_attribute("content")

# Print title and description
print(title)
print(description)


#Q2-2


# 關閉瀏覽器
driver.quit()