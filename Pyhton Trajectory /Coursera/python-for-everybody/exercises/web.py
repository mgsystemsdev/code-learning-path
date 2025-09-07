import urllib.request
import ssl
from bs4 import BeautifulSoup

# --- Ignore SSL certificate errors ---
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

# --- INPUTS ---
url = input('Enter URL: ')            # e.g., http://py4e-data.dr-chuck.net/known_by_Alysia.html
count = int(input('Enter count: '))   # e.g., 7
position = int(input('Enter position:  '))  # e.g., 18 (1-based index)

# --- MAIN LOOP ---
for i in range(count):
    print("Retrieving:", url)
    html = urllib.request.urlopen(url, context=ctx).read()
    soup = BeautifulSoup(html, 'html.parser')
    tags = soup('a')

    if position > len(tags):
        print(f"Error: only {len(tags)} links on this page, position {position} is out of range.")
        break

    url = tags[position - 1].get('href', None)

# --- FINAL NAME ---
print("Retrieving:", url)
name = url.split('_')[-1].split('.')[0]
print("The answer to the assignment is:", name)
