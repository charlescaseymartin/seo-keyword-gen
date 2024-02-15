from selenium.webdriver import Firefox
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup

# Scrape auto-suggestions
# auto-suggestion div class name: UUbT9 EyBRub
# auto-suggestion textarea id: APjFqb
# auto-suggestion ul class name: G43f7e
# auto-suggestion presentation span class name: wM6W7d

def get_current_page_element(browser: Firefox, attrs: dict[str] = {}):
  page_source = BeautifulSoup(browser.page_source, 'lxml')
  return page_source.find(attrs=attrs)


def extract_phrases(browser: Firefox):
  browser.get('https://www.google.com/')
  textarea = browser.find_element(By.CSS_SELECTOR, 'textarea#APjFqb')
  textarea.click()
  textarea.send_keys('test')
  attrs = { 'class': 'G43f7e' }
  auto_suggest_list_has_items = lambda children : len(list(children)) > 0
  # print(f'auto-suggest list tag: {auto_suggest_list_tag}')
  print(f'auto-suggest list has items [before]: {auto_suggest_list_has_items(get_current_page_element(browser=browser, attrs=attrs))}')
  print(f'auto-suggest list has items [after]: {auto_suggest_list_has_items(get_current_page_element(browser=browser, attrs=attrs))}')
  # print(f'Is auto-suggestion displayed: {auto_suggest_list.is_displayed()}')
  # textarea.send_keys('test')
  # # parsed_page = BeautifulSoup(browser.page_source, 'lxml')
  # print(f'Is auto-suggestion list displayed after keys:\n{is_auto_suggest_list_displayed}')


class GoogleScraper:
  current_url = 'https://www.google.com/'
