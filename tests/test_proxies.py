import unittest
import sys
from pathlib import Path
from selenium.webdriver.common.by import By

sys.path.append(str(Path(__file__).resolve().parent.parent))
from browser import WebBrowser


class TestProxies(unittest.TestCase):

    def test_proxy_works(self):
        webBrowser = WebBrowser()
        browser = webBrowser.browser
        current_proxy_addr = webBrowser.current_proxy.split(':')[2].split('@')[1]
        browser.get('https://ipinfo.io/')
        selector = 'li#ip-string div span.font-mono.block span.text-bali-hai-primary span.text-green-05'
        ip_addr = browser.find_element(By.CSS_SELECTOR, selector).text
        print(f'ip addr: {ip_addr} current proxy: {current_proxy_addr}')
        self.assertEqual(current_proxy_addr, ip_addr)

    def test_proxy_rotates(self):
        firstWebBrowserProxy = WebBrowser().current_proxy
        secondWebBrowserProxy = WebBrowser().current_proxy
        self.assertNotEqual(firstWebBrowserProxy, secondWebBrowserProxy)


if __name__ == '__main__':
    unittest.main()
