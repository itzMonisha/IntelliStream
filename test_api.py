import requests

r = requests.get("http://127.0.0.1:8000/analytics")

print("STATUS:", r.status_code)
print("TEXT:")
print(r.text)
