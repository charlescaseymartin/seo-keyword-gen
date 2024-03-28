import os

REMOTE_WEBDRIVER = 'http://selenium:4444/wd/hub'
root_path = os.getcwd()
DATA_DIR_PATH = f'{root_path}/data'
TOPICS_RESULTS_FILE_PATH = f'{DATA_DIR_PATH}/topic-authority.json'
PROXY_FILE_PATH = f'{DATA_DIR_PATH}/proxies.txt'
