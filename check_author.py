import requests
from bs4 import BeautifulSoup

url = 'http://books.toscrape.com/catalogue/sharp-objects_997/index.html'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

print('Looking for author information...')

# Check breadcrumb
breadcrumb = soup.select('.breadcrumb li')
print('Breadcrumb items:')
for item in breadcrumb:
    print(' ', item.text.strip())

# Check product info table
table = soup.find('table', class_='table')
if table:
    print('Product info table:')
    for row in table.find_all('tr'):
        print(' ', row.text.strip())

# Check if author is mentioned anywhere
text_content = soup.get_text().lower()
print('Author mentioned in text:', 'author' in text_content)

# Check meta tags
meta_tags = soup.find_all('meta')
print('Meta tags with author:')
for meta in meta_tags:
    if 'author' in str(meta).lower():
        print(' ', meta)