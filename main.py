from selenium import webdriver
from bs4 import BeautifulSoup
from constants import KEYWORDS_FILE

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
  with open(KEYWORDS_FILE, 'r+') as keyword_file:
    lines = [line.strip() for line in keyword_file.readlines()]
    for word in lines:
      if word not in keywords:
        keywords.append(word)
  return keywords

def scrape_seo_phrases(keywords = []):
  print('[*] Scrapping SEO Phrases related to main keywords')
  print(f'keywords to scrape: {keywords}')
  # scrape google
  # scrape ATP

if __name__ == '__main__':
  browser = create_browser_instance()
  KEYWORDS = load_keywords()
  scrape_seo_phrases(KEYWORDS)
  browser.quit()