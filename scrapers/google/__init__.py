from selenium.webdriver import Firefox
from .auto_suggestions import ExtractAutoSuggestions

def run(browser: Firefox, keywords):
  suggestionExtractor = ExtractAutoSuggestions(browser=browser, keywords=keywords)
  suggestionExtractor.run()