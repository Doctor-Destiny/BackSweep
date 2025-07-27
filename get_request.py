import requests
from urllib.parse import urlencode
import sys

# Get all command-line arguments passed to this script (excluding the script name)
args = sys.argv[1:]

if args:
    # For example: user ran `python script.py 123.45.67.89:8080`
    web_addr = args[0]

    # Example credentials and target
    url = web_addr
    username = "admin"
    password = "1234"

    # Parameters to be sent in GET (insecure method!)
    params = {
        "username": username,
        "password": password
    }

    # Create full URL with query parameters
    full_url = f"{url}?{urlencode(params)}"

    # Intercept-style print (like Burp)
    print("[Intercepted GET Request]")
    print(f"GET {full_url} HTTP/1.1")
    print("Host:", requests.utils.urlparse(url).netloc)
    print("User-Agent: Python/requests")
    print("Accept: */*")
    print()

    # Send the GET request
    response = requests.get(url, params=params)

    # Print response (optional)
    print("[Response]")
    print("Status Code:", response.status_code)
    print("Body:\n", response.text[:500])  # Print first 500 characters
