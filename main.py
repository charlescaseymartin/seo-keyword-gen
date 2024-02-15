from selenium import webdriver
from constants import KEYWORDS_FILE_PATH
from scrapers import google

def create_browser_instance():
  print('[*] Setting up browser instance')
  # Define options for running the firefox browser
  options = webdriver.FirefoxOptions()
  options.add_argument("--no-sandbox")
  options.add_argument("--headless")
  options.add_argument("--disable-dev-shm-usage")

  # Initialize a new firefox broswer instance
  return webdriver.Remote('http://core:4444/wd/hub', options=options)

def load_keywords():
  keywords = []
  # Read all keywords from file
  with open(KEYWORDS_FILE_PATH, 'r+') as keyword_file:
    lines = [line.strip() for line in keyword_file.readlines()]
    for word in lines:
      if word not in keywords:
        keywords.append(word)
  return keywords

if __name__ == '__main__':
  browser = create_browser_instance()
  main_keywords = load_keywords()
  print('[*] Scrapping SEO Phrases related to main keywords')
  # scrape ATP
  google.extract_phrases(browser)
  browser.quit()