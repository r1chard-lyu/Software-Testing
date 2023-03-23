from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

from selenium.webdriver.chrome.options import Options
options = Options()
options.add_argument('--headless')
options.add_argument('--window-size=1920,1080')
options.add_argument('--disable-gpu')
driver_path = ChromeDriverManager().install()
driver = webdriver.Chrome(executable_path=driver_path, options=options)



print(f"[*] Launch browser and navigate to NYCU home page")
driver.get("https://www.nycu.edu.tw/")

print(f"[*] Maximize the window and click \"新聞\" ")
driver.maximize_window()
news_link = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//a[@title='新聞']")))
news_link.click()


print(f"[*] Click first news ")
driver.find_element(By.CSS_SELECTOR,'.swiper-slide a').click()


print(f"[*] Print the title and content\n")
title = driver.title
print(f"Title : {title}")
contents = driver.find_elements(By.TAG_NAME, 'p')
print(f"Content : ")
for content in contents:
    print(content.text)


print(f"[*] Open a new tab")
driver.execute_script("window.open('');")

print(f"[*] Switch to the newly opened tab")
driver.switch_to.window(driver.window_handles[1])

print(f"[*] Navigate to google")
driver.get('https://www.google.com')


print("[*] Input your student number")
search_box = driver.find_element(By.NAME, "q")
search_box.send_keys("311555009")

print("[*] Submit the search query")
search_box.submit()

print("[*] Print the title of second result\n")
second_result = driver.find_elements(By.CSS_SELECTOR, "h3")
print(f"Title of Second Result for student id : \"{second_result[2].text}\"\n") 


print(f"[*] Close the browser\n")
driver.quit()


