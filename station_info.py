import json
import requests

# Search of all cities that starts with "ль"
headers = {'User-Agent':  'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:59.0) Gecko/20100101 Firefox/59.0'}
params = {"term": "ль"}
r = requests.post("https://booking.uz.gov.ua/train_search/station/", params=params, headers=headers)
response = json.loads(r.text)

print(json.dumps(response, sort_keys=True, indent=4, ensure_ascii=False))

# Search of all possible trains
data = {"from": "2218000", "to": "2200001", "date": "2018-06-09", "time": "00:00"}
r = requests.post("https://booking.uz.gov.ua/train_search/", data=data, headers=headers)
response = json.loads(r.text)

print(json.dumps(response, indent=4, ensure_ascii=False))
