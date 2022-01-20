#!/usr/bin/env python3
# coding: utf-8

import os
import sys

rundeck_weather_version = "0.3"

# Is Rundeck token present ?
try:
  os.environ['RD_TOKEN']
except:
  print("Token not found.")
  sys.exit(1)

token = "?authtoken=" + os.environ['RD_TOKEN']
urlbase = "http://rundeck.your-company.com/api/36"
url_rundeck = "http://rundeck.your-company.com/"
headers = {'Accept': 'application/json'}
headers_yaml = {'Accept': 'application/yaml', 'X-Rundeck-Auth-Token': os.environ['RD_TOKEN']}
