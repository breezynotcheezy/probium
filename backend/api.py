import requests

API_URL = "http://192.168.30.77:8000/api/v1/scan/file"

with open("scanned.csv", "rb") as f:
    files = {"file": ("scanned.csv", f)}
    resp = requests.post(API_URL, files=files)
    print(resp.json())
