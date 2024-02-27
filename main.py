from selenium import webdriver
from constants import REMOTE_WEBDRIVER, KEYWORDS_FILE_PATH
from utils import wait_for_selenium_to_start
from scrapers import google

def create_browser_instance():
  print('[*] Setting up browser instance...')
  options = webdriver.FirefoxOptions()
  options.add_argument("--no-sandbox")
  options.add_argument("--headless")
  options.add_argument("--disable-dev-shm-usage")
  return webdriver.Remote(REMOTE_WEBDRIVER, options=options)

def load_keywords():
  keywords = []
  with open(KEYWORDS_FILE_PATH, 'r+') as keyword_file:
    lines = [line.strip() for line in keyword_file.readlines()]
    [keywords.append(word) for word in lines if word not in keywords]
  return keywords

if __name__ == '__main__':
  wait_for_selenium_to_start()
  browser = create_browser_instance()
  keywords = load_keywords()
  print('[*] Extracting related topics from keywords...')
  # # scrape ATP
  google.run(browser, keywords)
  browser.quit()