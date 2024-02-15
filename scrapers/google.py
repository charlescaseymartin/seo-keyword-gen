from selenium.webdriver import Firefox
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from time import sleep
from constants import DATA_DIR_PATH

google_home_page_url = 'https://www.google.com/'
google_search_url = 'https://www.google.com/search?q='

def get_current_page_element(browser: Firefox, attrs: dict[str] = {}):
  page_source = BeautifulSoup(browser.page_source, 'lxml')
  return page_source.find(attrs=attrs)

# Scrape auto-suggestions
# auto-suggestion div class name: aajZCb
# auto-suggestion textarea id: APjFqb
# auto-suggestion ul class name: G43f7e
# auto-suggestion presentation span class name: wM6W7d
def extract_auto_suggest_phrases(browser: Firefox, main_keywords = []):
  browser.get(google_home_page_url)
  textarea = browser.find_element(By.CSS_SELECTOR, 'textarea#APjFqb')
  attrs = { 'class': 'G43f7e' }
  
  # auto_suggest_list_has_items = lambda children : len(list(children)) > 0
  # print(f'auto-suggest list has items: {auto_suggest_list_has_items()}')

  for keyword in main_keywords:
  #   for pattern in [lambda x:x, lambda x:x, lambda x:x]:
  #     keyword_patterns = pattern(keyword)
  #     for key_pattern in keyword_patterns:
    try:
      textarea.click()
      textarea.send_keys('test ')
      # browser.implicitly_wait(5)
      sleep(1)
      auto_suggest_list = get_current_page_element(browser=browser, attrs=attrs)
      auto_suggestions = [suggestion.contents[0].contents[1].contents[0].contents[0].contents[0] for suggestion in auto_suggest_list.contents]
      # auto_suggestions = [suggestion_item.stripped_strings for suggestion_item in auto_suggestions]
      # textarea.click()
      print(f'auto-suggestions list item: {auto_suggestions}')
    except Exception as err:
      print(f'Unexpected {err}, {type(err)=}')


def extract_phrases(browser: Firefox, main_keywords = []):
  extract_auto_suggest_phrases(browser=browser, main_keywords=main_keywords)