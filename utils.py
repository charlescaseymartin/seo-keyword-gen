import requests
import time
from constants import REMOTE_WEBDRIVER

def get_selenium_status():
  try:
    response = requests.get(f'{REMOTE_WEBDRIVER}/status').json()
    status = response['value']['ready'] if response else False
    return status
  except Exception as err:
    return False

def wait_for_selenium_to_start():
  print(f'[*] Waiting until Selenium is ready...')
  while get_selenium_status() is not True:
    time.sleep(5)
  print(f'[*] Selenium is ready!')