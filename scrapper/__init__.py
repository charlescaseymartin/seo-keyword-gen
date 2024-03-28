import urllib.parse
import sys
from selenium.webdriver import Firefox
from selenium.webdriver.common.by import By
from browser import WebBrowser

# search auto-suggestions
# extract the people also asked questions for each search result
# extract the related searches for each search result
# extract the top 5 results for each search
# result container selector: div.g.Ww4FFb.vt6azd.tF2Cxc.asEBEc
# result links selector: a[jsname="UWckNb"]
# extract the following for each top result:
#   - meta description
#   - meta keywords
#   - schema mark up
#   - canonical tag
#   - header tag
#   - image alt description
#   - xml sitemap
#   - robots.txt
#   - html structure
#   - keyword density

browser = WebBrowser().browser
BASE_URL = 'https://www.google.com/search?'
BOT_CHECK_URL = 'https://www.google.com/sorry/index'

def get_top_pages(browser: Firefox):
    results = browser.find_elements(By.CSS_SELECTOR, 'div.g.Ww4FFb.vt6azd.tF2Cxc.asEBEc')
    print(results)

def topic_search(topic: str):
    params = urllib.parse.urlencode({ 'q': topic })
    url = f'{BASE_URL}{params}'
    browser.get(url)

        if BOT_CHECK_URL in browser.current_url:
            print('[*] Blocked by robot check')
            browser = WebBrowser().browser
            topic_search(topic)

    print(f'current title: {browser.title}')
    print(f'current url: {browser.current_url}')
    #get_top_pages(browser)

def search_topics(topics: list[str]):
    print('[*] Starting search')
    for topic in topics:
        topic_search(topic)
