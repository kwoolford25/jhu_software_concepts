from urllib import parse, robotparser
import json

agent = 'Kyle'
url = "https://api.weather.gov/gridpoints/LWX/96,70/forecast/hourly"

# Parser setup
parser = robotparser.RobotFileParser(url)
parser.set_url(parse.urljoin(url, 'robots.txt'))

paths = [
    "/",
    "/cgi-bin/",
    "/admin/",
    "survey/?program=Computer+Science"
]

for path in paths:
    print(f"{parser.can_fetch(agent, path), path}")