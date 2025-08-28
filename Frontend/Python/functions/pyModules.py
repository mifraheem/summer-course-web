import random

# print(random.random())
# print(random.randint(1, 50))

import datetime
# from datetime import now
print(datetime.date(2025, 4, 20))
print(datetime.datetime.now())
print(datetime.date.today())

import requests
url = "https://ifraheem.com"
data = requests.request(url=url, method="GET")
print(data)