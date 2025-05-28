import re

string = "Welcome tn EN605.256: modern software concepts in Python!"

print(re.search("[A-Za-z]{2}[0-9]*\.[0-9]+", string))