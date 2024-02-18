#!/bin/bash
SELENIUM_HOST='core'

echo "[*] Waiting for Selenium host to ready up::$SELENIUM_HOST"
while [ "$( curl -s http://$SELENIUM_HOST:4444/wd/hub/status | jq -r .value.ready )" != "true" ]
do
    sleep 1
done
echo "[*] Selenium host is ready!"

python main.py >> ./data/logs.txt