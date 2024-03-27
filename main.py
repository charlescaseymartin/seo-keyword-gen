import sys
import os
from selenium import webdriver
from common.constants import REMOTE_WEBDRIVER
from common.utils import wait_for_selenium_to_start
import scrappers

def create_browser_instance():
    options = webdriver.FirefoxOptions()
    options.add_argument("--no-sandbox")
    options.add_argument("--headless")
    options.add_argument("--disable-dev-shm-usage")
    return webdriver.Remote(REMOTE_WEBDRIVER, options=options)

def invalid_keyword_file():
    print('Invalid keyword file. Read help menu for more')
    sys.exit(1)

def load_keywords(key_path:str):
    if len(key_path) > 0 and os.path.isfile(key_path) == False:
        invalid_keyword_file()
    keywords = []
    with open(key_path, 'r+') as keyword_file:
        lines = [line.strip().split(',') for line in keyword_file.readlines()]
        keywords = [keyword.strip() for row in lines for keyword in row if len(keyword) > 1]
    if len(keywords) < 1:
        invalid_keyword_file()
    return keywords

def usage():
    print('''This is the help menu for Topic Authority Generator!

    -h          Shows this menu

    -k [path]   A text file (.txt) containing coma separated list of
                keywords to generate topic authority''')

if __name__ == '__main__':
    args = sys.argv
    if len(args) > 1 and args[1] == '-k' and 2 < len(args):
        keywords = load_keywords(key_path=args[2])
        print('[*] Extracted keyword/s')
        wait_for_selenium_to_start()
        browser = create_browser_instance()
        print('[*] Browser is ready')
        scrappers.run(browser, keywords)
        browser.quit()
    else:
        usage()
