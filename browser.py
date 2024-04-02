import random
from selenium import webdriver
from common.constants import REMOTE_WEBDRIVER, PROXY_FILE_PATH
from common.utils import wait_for_selenium_to_start

proxy_list = []
with open(PROXY_FILE_PATH, 'r+') as proxy_file:
    lines = [line.strip().split(',') for line in proxy_file.readlines()]
    proxy_list = [proxy for row in lines for proxy in row if len(proxy) > 1]
    proxy_list = [proxy.strip() for proxy in proxy_list]


class WebBrowser:
    options = webdriver.FirefoxOptions()
    current_proxy = ''

    def __init__(self):
        self.set_default_options()
        wait_for_selenium_to_start()
        self.browser = webdriver.Remote(REMOTE_WEBDRIVER, options=self.options)
        print('[*] Browser is ready')

    def set_default_options(self):
        self.options.add_argument('--no-sandbox')
        self.options.add_argument('--headless')
        self.options.add_argument('--disable-dev-shm-usage')
        self.add_proxy()

    def add_proxy(self):
        proxy = random.choice(proxy_list)
        if len(self.current_proxy) > 0:
            while proxy == self.current_proxy:
                proxy = random.choice(proxy_list)
        self.current_proxy = proxy
        print(f'selected proxy: {proxy}')
        # self.options.add_argument(f'--proxy-server={proxy}')
