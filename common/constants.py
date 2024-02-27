import os

REMOTE_WEBDRIVER = 'http://core:4444/wd/hub'
root_path = os.getcwd()
DATA_DIR_PATH = f'{root_path}/data'
KEYWORDS_FILE_PATH = f'{DATA_DIR_PATH}/keywords.txt'
TOPICS_RESULTS_FILE_PATH = f'{DATA_DIR_PATH}/topic-authority.json'