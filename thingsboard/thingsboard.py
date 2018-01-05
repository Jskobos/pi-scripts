#!/usr/bin/env python

import json
import requests
import logging
import os
from sense_hat import SenseHat
from time import sleep
from os.path import join, dirname
from dotenv import load_dotenv

# Load environment variables

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

# Configure log file

#logging.basicConfig(filename='/home/jkobos/thingsboard.log', level=logging.WARNING, format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')

# Load constants from external .env file.

API_KEY          = os.environ.get("API_KEY")
THINGSBOARD_HOST = os.environ.get("THINGSBOARD_HOST")

thingsboard_url  = "http://{0}/api/v1/{1}/telemetry".format(THINGSBOARD_HOST, API_KEY)

sense = SenseHat()


data = {}

while True:
    data['temperature'] = sense.get_temperature()
    data['pressure']    = sense.get_pressure()
    data['humidity']    = sense.get_humidity()

    r = requests.post(thingsboard_url, data=json.dumps(data)) 
    print(str(data))
    status = r.status_code
    if status is not 200:
        logging.warning(str(status) + ': ' + str(data))
    sleep(60)
