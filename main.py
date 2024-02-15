from selenium import webdriver
from selenium.webdriver.common.by import By

# Define options for running the firefoxdriver
print('[*] Setting up browser options...')
options = webdriver.FirefoxOptions()
options.add_argument("--no-sandbox")
options.add_argument("--headless")
options.add_argument("--disable-dev-shm-usage")

# Initialize a new firefox driver instance
print('[*] Setting up browser instance...')
driver = webdriver.Remote('http://core:4444/wd/hub', options=options)
driver.get('https://www.google.com/')
page_title = driver.title

print(f'current page title: {page_title}')

driver.quit()

# print('[!] STARTED SCRIPT!!!')