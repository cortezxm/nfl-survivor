import requests, os

url = "https://api.balldontlie.io/nfl/v1/players"
headers = {"Authorization": os.environ["BALLDONTLIE_API_KEY"]}

params = {"per_page": 25}
resp = requests.get(url, headers=headers, params=params, timeout=10)
print(resp.status_code)
resp.raise_for_status()
body = resp.json()

bookmark = body["meta"]["next_cursor"]
first1 = body["data"][0]["last_name"]
print(f"{first1}")
print(bookmark)

params2 = {"per_page": 25, "cursor": bookmark}
resp2 = requests.get(url, headers=headers, params=params2, timeout=10)
resp2.raise_for_status()
body2 = resp2.json()

bookmark2 = body2["meta"]["next_cursor"]
first2 = body2["data"][0]["last_name"]
print(f"{first2}")
print(bookmark2)