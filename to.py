import requests

url = 'https://www.w3schools.com/python/demopage.php'
BODY = {'NumbersOfRows': 'NubersOfColumns'}

x = requests.post(url, data = BODY)

print(x.text)