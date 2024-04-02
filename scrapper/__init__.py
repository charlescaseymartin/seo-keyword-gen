import urllib.parse
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


class ScrapeTopResults:
    browser = WebBrowser().browser
    BASE_URL = 'https://www.google.com/search?'
    BOT_CHECK_URL = 'https://www.google.com/sorry/index'

    def get_top_pages(self):
        selector = 'div.g.Ww4FFb.vt6azd.tF2Cxc.asEBEc'
        results = self.browser.find_elements(By.CSS_SELECTOR, selector)
        print(results)

    def topic_search(self, topic: str):
        params = urllib.parse.urlencode({'q': topic})
        url = f'{self.BASE_URL}{params}'
        self.browser.get(url)
        if self.BOT_CHECK_URL in self.browser.current_url:
            print('[*] Blocked by robot check')
            self.browser = WebBrowser().browser
            self.topic_search(topic)
        print(f'current title: {self.browser.title}')
        print(f'current url: {self.browser.current_url}')
        # get_top_pages(browser)

    def search_topics(self, topics: list[str]):
        print('[*] Starting search')
        for topic in topics:
            self.topic_search(topic)
