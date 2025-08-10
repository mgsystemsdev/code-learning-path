import urllib.request
import xml.etree.ElementTree as ET

# Hardcoded URL for the assignment
url = 'http://py4e-data.dr-chuck.net/comments_2208428.xml'

print('Retrieving', url)
uh = urllib.request.urlopen(url)
data = uh.read()
print('Retrieved', len(data), 'characters')

# Parse XML
tree = ET.fromstring(data)
counts = tree.findall('.//count')

# Extract and sum up counts
nums = []
for count in counts:
    value = int(count.text)
    nums.append(value)

# Final output
print('Count:', len(nums))
print('Sum:', sum(nums))
