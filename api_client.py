import requests, os

url = "https://api.balldontlie.io/nfl/v1/teams"
headers = {"Authorization": os.environ["BALLDONTLIE_API_KEY"]}

resp = requests.get(url, headers=headers, timeout=10)
print(resp.status_code)
resp.raise_for_status()
body = resp.json()
print(type(body))

teams = body["data"]
print(len(teams))
print(teams[0]["full_name"])