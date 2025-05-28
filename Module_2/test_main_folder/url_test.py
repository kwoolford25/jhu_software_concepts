from urllib.request import urlopen
import json

url = "https://api.weather.gov/gridpoints/LWX/96,70/forecast/hourly"

page = urlopen(url)

html_bytes = page.read()

washington_weather = json.loads(html_bytes)

print(f"Current Temperature in D.C is {washington_weather['properties']['periods'][0]['temperature']}")