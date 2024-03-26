from selenium.webdriver import Firefox
from selenium.webdriver.common.by import By
from time import sleep
from string import ascii_lowercase
from common.utils import save_results_to_file

class ExtractAutoSuggestions:
    browser: Firefox
    keyword_topics: dict
    keywords: list[str]

    def __init__(self, browser: Firefox, keywords: list[str]):
        self.browser = browser
        self.keywords = keywords
        self.browser.get('https://www.google.com/')
        self.keyword_topics = {}

    def run(self):
        print(self.keywords)
        self.textarea = self.browser.find_element(By.CSS_SELECTOR, 'textarea#APjFqb')
        self.default_topics = self.get_default_topics()
        for keyword in self.keywords:
           self.add_topics_keywords(keyword, self.get_topic_suggestions(keyword))
           self.get_alphabetic_started_topics(keyword)
           self.get_alphabetic_ended_topics(keyword)
           self.get_alphabetic_started_and_ended_topics(keyword)
           self.get_alphabetic_started_and_double_ended_topics(keyword)
           self.get_question_topics(keyword)
           self.get_popular_topics(keyword)
           keyword_key = keyword.replace(' ', '_')
           self.keyword_topics[keyword_key] = list(set(self.keyword_topics[keyword_key]))
        save_results_to_file('auto_suggestions', self.keyword_topics)

    def get_default_topics(self):
        default_topics = set()
        try:
            self.textarea.click()
            suggestions = self.browser.find_elements(By.CSS_SELECTOR, 'div.wM6W7d span')
            default_topics = set([suggestion.text for suggestion in suggestions if suggestion.text])
            return default_topics
        except Exception as err:
            print(f'Unexpected {err}, {type(err)=}')
            return default_topics

    def get_topic_suggestions(self, keyword_pattern: str):
        suggestions_topics = []
        try:
            assert len(keyword_pattern) > 1
            self.textarea.click()
            self.textarea.clear()
            self.textarea.send_keys(keyword_pattern)
            sleep(2)
            suggestions = self.browser.find_elements(By.CSS_SELECTOR, 'div.wM6W7d span')
            suggestions_topics = [suggestion.text for suggestion in suggestions if suggestion.text]

            is_focused_suggestion = self.is_focused_suggestions()
            if is_focused_suggestion:
                focused_suggestions = self.browser.find_elements(By.CSS_SELECTOR, 'div.wM6W7d span b')
                suggestions_topics = [f"{keyword_pattern}{suggestion.text}" for suggestion in focused_suggestions]

            default_topic_check = self.default_topics.union(set(suggestions_topics))
            if len(default_topic_check) == len(self.default_topics):
                suggestions_topics = self.get_topic_suggestions(keyword_pattern=keyword_pattern)

            return suggestions_topics
        except Exception as err:
            print(f'Unexpected {err}, {type(err)=}')
            return suggestions_topics

    def is_focused_suggestions(self):
        input_container = self.browser.find_element(By.CSS_SELECTOR, 'div.RNNXgb')
        suggestion_list = self.browser.find_element(By.CSS_SELECTOR, 'ul.G43f7e')
        input_container_size = input_container.size['width']
        suggestion_list_size = suggestion_list.size['width']
        return suggestion_list_size < input_container_size

    def add_topics_keywords(self, keyword: str, pattern_topics: list):
        keyword_key = keyword.replace(' ', '_')
        if keyword_key in self.keyword_topics.keys():
            self.keyword_topics[keyword_key].extend(pattern_topics)
        else:
            self.keyword_topics[keyword_key] = pattern_topics

    def get_alphabetic_started_topics(self, keyword: str):
        key_patterns = [f'{letter} {keyword}' for letter in ascii_lowercase]
        pattern_topics = []
        [pattern_topics.extend(self.get_topic_suggestions(key_pattern)) for key_pattern in key_patterns]
        self.add_topics_keywords(keyword, pattern_topics)
        print(f'[*] Extracted alphabetical started topics for: {keyword}')

    def get_alphabetic_ended_topics(self, keyword: str):
        key_patterns = [f'{keyword} {letter}' for letter in ascii_lowercase]
        pattern_topics = []
        [pattern_topics.extend(self.get_topic_suggestions(key_pattern)) for key_pattern in key_patterns]
        self.add_topics_keywords(keyword, pattern_topics)
        print(f'[*] Extracted alphabetical ended topics for: {keyword}')

    def get_alphabetic_started_and_ended_topics(self, keyword: str):
        key_patterns = [f'{letter} {keyword} {letter}' for letter in ascii_lowercase]
        pattern_topics = []
        [pattern_topics.extend(self.get_topic_suggestions(key_pattern)) for key_pattern in key_patterns]
        self.add_topics_keywords(keyword, pattern_topics)
        print(f'[*] Extracted alphabetical started and ended topics for: {keyword}')

    def get_alphabetic_started_and_double_ended_topics(self, keyword: str):
        key_patterns = [f'{letter} {keyword} {letter}{letter}' for letter in ascii_lowercase]
        pattern_topics = []
        [pattern_topics.extend(self.get_topic_suggestions(key_pattern)) for key_pattern in key_patterns]
        self.add_topics_keywords(keyword, pattern_topics)
        print(f'[*] Extracted alphabetical started and double ended topics for: {keyword}')

    def get_question_topics(self, keyword: str):
        questions = ['how', 'how to', 'how do', 'why do', 'what', 'is', 'do', 'does a']
        key_patterns = [f'{question} {keyword}' for question in questions]
        pattern_topics = []
        [pattern_topics.extend(self.get_topic_suggestions(key_pattern)) for key_pattern in key_patterns]
        self.add_topics_keywords(keyword, pattern_topics)
        print(f'[*] Extracted question topics for: {keyword}')

    def get_popular_topics(self, keyword: str):
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
        key_patterns = [phrase.replace('<keyword>', keyword) for phrase in popular_phrases]
        pattern_topics = []
        [pattern_topics.extend(self.get_topic_suggestions(key_pattern)) for key_pattern in key_patterns]
        self.add_topics_keywords(keyword, pattern_topics)
        print(f'[*] Extracted popular topics for: {keyword}')
