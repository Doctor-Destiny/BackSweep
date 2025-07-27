import requests
import sys

# Get all command-line arguments passed to this script (excluding the script name)
args = sys.argv[1:]

if args:
    # For example: user ran `python script.py 123.45.67.89:8080`
    web_addr = args[0]

    # Target login URL
    url = web_addr

    # Login credentials
    username = "admin"
    password = "1234"

    # Data to be sent in the body of the POST request
    data = {
        "username": username,
        "password": password
    }

    # Headers to mimic a real browser request (optional)
    headers = {
        "User-Agent": "Python/requests",
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept": "*/*"
    }

    # Interceptor-style print
    print("[Intercepted POST Request]")
    print(f"POST {url} HTTP/1.1")
    print("Host:", requests.utils.urlparse(url).netloc)
    for k, v in headers.items():
        print(f"{k}: {v}")
    print()
    print("&".join(f"{k}={v}" for k, v in data.items()))
    print()

    # Send the POST request
    response = requests.post(url, data=data, headers=headers)

    # Print response
    print("[Response]")
    print("Status Code:", response.status_code)
    print("Body:\n", response.text[:500])  # First 500 chars of response
