import requests
import time
import os
import json
from common.constants import REMOTE_WEBDRIVER, TOPICS_RESULTS_FILE_PATH

def get_selenium_status():
  try:
    response = requests.get(f'{REMOTE_WEBDRIVER}/status').json()
    status = response['value']['ready'] if response else False
    return status
  except Exception:
    return False

def wait_for_selenium_to_start():
  while get_selenium_status() is not True:
    time.sleep(5)

def save_results_to_file(key, data):
  if os.path.exists(TOPICS_RESULTS_FILE_PATH):
    existing_data = {}
    with open(TOPICS_RESULTS_FILE_PATH, 'r+') as json_file:
      existing_data = json.load(json_file)
    open(TOPICS_RESULTS_FILE_PATH, 'w').close()
    with open(TOPICS_RESULTS_FILE_PATH, 'w+') as json_file:
      if key in existing_data.keys():
        existing_data[key].update(data)
      else:
        existing_data[key] = data
      new_data = json.dumps(existing_data, indent=4)
      json_file.write(new_data)
  else:
    with open(TOPICS_RESULTS_FILE_PATH, 'x') as json_file:
      new_data = json.dumps({key: data}, indent=4)
      json_file.write(new_data)
