import urllib.request
import json

# Use your actual data URL
url = 'http://py4e-data.dr-chuck.net/comments_2208429.json'

print('Retrieving', url)
data = urllib.request.urlopen(url).read()
print('Retrieved', len(data), 'characters')

# Load JSON and parse
info = json.loads(data)

# Extract counts and compute the sum
counts = [item['count'] for item in info['comments']]

print('Count:', len(counts))
print('Sum:', sum(counts))
