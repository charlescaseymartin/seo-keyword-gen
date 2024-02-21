from selenium.webdriver import Firefox
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from bs4 import BeautifulSoup
from time import sleep
from string import ascii_lowercase
from utils import wait_for_selenium_to_start

# Scrape auto-suggestions
# form input div class name: RNNXgb
# auto-suggestion styled container div class name: UUbT9 EyBRub
# auto-suggestion textarea id: APjFqb
# auto-suggestion ul class name: G43f7e
# auto-suggestion presentation span class name: wM6W7d

class ExtractAutoSuggestions:
  browser: Firefox
  keyword_topics = {}
  keywords = []

  def __init__(self, browser: Firefox, keywords = []):
    self.browser = browser
    self.keywords = keywords
    self.browser.get('https://www.google.com/')
    pass

  def run(self):
    self.textarea = self.browser.find_element(By.CSS_SELECTOR, 'textarea#APjFqb')
    pattern_generators = [
      self.generate_alphabetic_started_key_phrases,
      self.generate_alphabetic_ended_key_phrases,
      self.generate_alphabetic_started_and_ended_key_phrases,
      self.generate_alphabetic_started_and_double_ended_key_phrases,
      self.generate_question_key_phrases,
      self.generate_popular_key_phrases
    ]

    
    for keyword in self.keywords:
      keyword_key = str(keyword).replace(' ', '_')
      self.keyword_topics[keyword_key] = self.get_topic_suggestions(keyword)
      # keyword_patterns = []
      # [keyword_patterns.extend(gen_patterns(keyword)) for gen_patterns in pattern_generators]
      # print(f'keyword_patterns: {keyword_patterns}')

      alpha_started_key_patterns = self.generate_alphabetic_started_key_phrases
      alpha_ended_key_patterns = self.generate_alphabetic_ended_key_phrases
      alpha_started_and_ended_key_patterns = self.generate_alphabetic_started_and_ended_key_phrases
      alpha_started_and_double_ended_key_patterns = self.generate_alphabetic_started_and_double_ended_key_phrases
      question_key_patterns = self.generate_question_key_phrases
      popular_key_patterns = self.generate_popular_key_phrases
      # for key_pattern in keyword_patterns:
      # print(f'[*] Current keyword pattern: {key_pattern}')
      key_pattern_suggestions = []
      [key_pattern_suggestions.extend(self.get_topic_suggestions(key_pattern)) for key_pattern in alpha_started_key_patterns]
      print(f'key_pattern_suggestions: {key_pattern_suggestions}')
      # if self.keyword_topics[keyword_key] is not None:
      #   self.keyword_topics[keyword_key].extend(key_pattern_suggestions) 
      # else:
      #   self.keyword_topics[keyword_key] = key_pattern_suggestions

    print(f'keyword topics: {self.keyword_topics}')

  def get_topic_suggestions(self, keyword_pattern = ''):
    try:
      assert len(keyword_pattern) > 1
      self.textarea.clear()
      self.textarea.click()
      self.textarea.send_keys(keyword_pattern)
      sleep(2)
      suggestions = self.browser.find_elements(By.CSS_SELECTOR, 'div.wM6W7d span')
      suggestions_topics = [suggestion.text for suggestion in suggestions if suggestion.text]
      is_focused_suggestion = self.is_focused_suggestions()

      if is_focused_suggestion:
        focused_suggestions = self.browser.find_elements(By.CSS_SELECTOR, 'div.wM6W7d span b')
        suggestions_topics = [f"{keyword_pattern}{suggestion.text}" for suggestion in focused_suggestions]

      return suggestions_topics
    except Exception as err:
      print(f'Unexpected {err}, {type(err)=}')
  
  def is_focused_suggestions(self):
    input_container = self.browser.find_element(By.CSS_SELECTOR, 'div.RNNXgb')
    suggestion_list = self.browser.find_element(By.CSS_SELECTOR, 'ul.G43f7e')
    input_container_size = input_container.size['width']
    suggestion_list_size = suggestion_list.size['width']
    return suggestion_list_size < input_container_size

  def generate_alphabetic_started_key_phrases(self, keyword: str):
    return [f'{letter} {keyword}' for letter in ascii_lowercase]

  def generate_alphabetic_ended_key_phrases(self, keyword: str):
    return [f'{keyword} {letter}' for letter in ascii_lowercase]

  def generate_alphabetic_started_and_ended_key_phrases(self, keyword: str):
    return [f'{letter} {keyword} {letter}' for letter in ascii_lowercase]

  def generate_alphabetic_started_and_double_ended_key_phrases(self, keyword: str):
    return [f'{letter} {keyword} {letter}{letter}' for letter in ascii_lowercase]

  def generate_question_key_phrases(self, keyword: str):
    questions = ['how', 'how to', 'how do', 'why do', 'what', 'is', 'do', 'does a']
    return [f'{question} {keyword}' for question in questions]

  def generate_popular_key_phrases(self, keyword: str):
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
  
