from selenium.webdriver import Firefox
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from bs4 import BeautifulSoup
from time import sleep
from string import ascii_lowercase
import array as arr

google_home_page_url = 'https://www.google.com/'
google_search_url = 'https://www.google.com/search?q='

def get_current_page_element(browser: Firefox, attrs: dict[str] = {}):
  page_source = BeautifulSoup(browser.page_source, 'lxml')
  return page_source.find(attrs=attrs)

def generate_alphabetic_started_key_phrases(keyword: str):
  return [f'{letter} {keyword}' for letter in ascii_lowercase]

def generate_alphabetic_ended_key_phrases(keyword: str):
  return [f'{keyword} {letter}' for letter in ascii_lowercase]

def generate_alphabetic_started_and_ended_key_phrases(keyword: str):
  return [f'{letter} {keyword} {letter}' for letter in ascii_lowercase]

def generate_alphabetic_started_and_double_ended_key_phrases(keyword: str):
  return [f'{letter} {keyword} {letter}{letter}' for letter in ascii_lowercase]

def generate_question_key_phrases(keyword: str):
  questions = ['how', 'how to', 'how do', 'why do', 'what', 'is', 'do', 'does a']
  return [f'{question} {keyword}' for question in questions]

def generate_popular_key_phrases(keyword: str):
  popular_phrases = [
    'Best <keyword> *',
    'Best <keyword> for *',
    'Best * for <keyword>',
    'Top <keyword> *',
    'Top 10 <keyword> *',
    '<keyword> or *',
    '<keyword> vs *',
    '<keyword> * reviews'
  ]
  return [phrase.replace('<keyword>', keyword) for phrase in popular_phrases]

# Scrape auto-suggestions
# form input div class name: RNNXgb
# auto-suggestion styled container div class name: UUbT9 EyBRub
# auto-suggestion textarea id: APjFqb
# auto-suggestion ul class name: G43f7e
# auto-suggestion presentation span class name: wM6W7d

def is_focused_auto_suggestions_displayed(browser: Firefox):
  input_container = browser.find_element(By.CSS_SELECTOR, 'div.RNNXgb')
  suggestion_list = browser.find_element(By.CSS_SELECTOR, 'ul.G43f7e')
  input_container_size = input_container.size['width']
  suggestion_list_size = suggestion_list.size['width']
  return suggestion_list_size < input_container_size 

def parse_suggestion_items(suggestions=[]):
  replace_encodings = lambda suggestion: str(suggestion).replace('<span>', '').replace('</span>', '').replace('<b>', '').replace('</b>', '').replace('\xa0', ' ')
  return [replace_encodings(suggestion) for suggestion in suggestions if len(str(suggestion)) > 0]

def get_suggestion_text_container(suggestion_list_item):
  return suggestion_list_item.contents[0].contents[1].contents[0].contents[0].contents[0]

def get_auto_suggestions(auto_suggest_list_contents=[]):
  suggestions = [get_suggestion_text_container(suggestion) for suggestion in auto_suggest_list_contents]
  # print(f'suggestions: {suggestions}')
  return parse_suggestion_items(suggestions=suggestions)

def get_focused_auto_suggestions(keyword='', auto_suggest_list_contents=[]):
  suggestions = [get_suggestion_text_container(suggestion).b for suggestion in auto_suggest_list_contents if get_suggestion_text_container(suggestion).b is not None]
  # print(f'suggestions: {suggestions}')
  parsed_suggestions = parse_suggestion_items(suggestions=suggestions)
  return [f'{keyword}{suggestion_item}' for suggestion_item in parsed_suggestions]

def get_suggestions(browser: Firefox, textarea: WebElement, attrs={}, key_pattern=''):
  try:
    assert len(key_pattern) > 1
    textarea.clear()
    textarea.click()
    textarea.send_keys(key_pattern)
    browser.implicitly_wait(3)
    # sleep(1)
    auto_suggest_list = get_current_page_element(browser=browser, attrs=attrs).contents

    if is_focused_auto_suggestions_displayed(browser=browser):
      print(f'is focused suggestions: {is_focused_auto_suggestions_displayed(browser=browser)}')
      auto_suggestions = get_focused_auto_suggestions(keyword=key_pattern, auto_suggest_list_contents=auto_suggest_list)
    else:
      auto_suggestions = get_auto_suggestions(auto_suggest_list)
    
    return auto_suggestions
  except Exception as err:
    print(f'Unexpected {err}, {type(err)=}')

def extract_auto_suggest_phrases(browser: Firefox, main_keywords = []):
  browser.get(google_home_page_url)
  textarea = browser.find_element(By.CSS_SELECTOR, 'textarea#APjFqb')
  attrs = { 'class': 'G43f7e' }
  key_phrases = {}
  pattern_generators = [
    generate_alphabetic_started_key_phrases,
    generate_alphabetic_ended_key_phrases,
    generate_alphabetic_started_and_ended_key_phrases,
    generate_alphabetic_started_and_double_ended_key_phrases,
    generate_question_key_phrases,
    generate_popular_key_phrases
  ]
  
  suggestions = get_suggestions(browser=browser, textarea=textarea, attrs=attrs, key_pattern='jaslkdj hd')
  print(f'test focused suggestions: {suggestions}')

  # for keyword in main_keywords:
  # keyword = main_keywords[0]
  # print(f'[*] Extracting auto-suggestions for {keyword}...')
  # suggestions = get_suggestions(browser=browser, textarea=textarea, attrs=attrs, key_pattern=keyword)
  # key_phrases[keyword] = suggestions
  # for pattern_generator in pattern_generators:
  #   keyword_patterns = pattern_generator(keyword)
  #   for key_pattern in keyword_patterns:
  #     print(f'key_pattern: {key_pattern}')
  #     key_pattern_suggestions = get_suggestions(browser=browser, textarea=textarea, attrs=attrs, key_pattern=key_pattern)
  #     print(f'key_pattern_suggestions: {key_pattern_suggestions}')
  #     key_phrases[keyword].extend(key_pattern_suggestions)

  # print(f'key_phrases: {key_phrases}')


def extract_phrases(browser: Firefox, main_keywords = []):
  extract_auto_suggest_phrases(browser=browser, main_keywords=main_keywords)