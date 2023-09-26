import cloudscraper
from bs4 import BeautifulSoup
import json
scraper = cloudscraper.create_scraper(delay=10, browser="chrome")

base_url = 'https://www.chabad.org/library/article_cdo/aid/2301647/jewish/Life-and-Times.html'
response = scraper.get(base_url).text
soup = BeautifulSoup(response, 'html.parser')
for blockquote in soup.find_all('blockquote'):
    blockquote.decompose()
for tag in soup.find_all(class_="article-toc padding"):
    tag.decompose()


# Extract author and name
author = "J. Immanuel Schochet"
name = "Life and Times of the Baal Shem Tov"

# Extract author and name
author = "J. Immanuel Schochet"
name = "Life and Times of the Baal Shem Tov"

# Extract parts and their associated texts
headers = soup.find_all('h2')
data = []

# Handle the first part without a header
first_text_paragraphs = [p.text.strip() for p in soup.find_all('p', limit=len(headers[0].find_all_previous('p')))]
data.append({
    "author": author,
    "name": name,
    "part": "",
    "text": "\n".join(first_text_paragraphs).strip()
})

# Handle the remaining parts with headers
for header in headers:
    part = header.text.strip()
    text_paragraphs = []
    
    # Extract text until the next header or end of the content
    for sibling in header.find_all_next():
        if sibling.name and sibling.name == 'h2':
            break
        if sibling.name == 'p' and not sibling.has_attr('class'):
            text_paragraphs.append(sibling.text.strip())

    text = "\n".join(text_paragraphs).strip()
    if (not text):
        continue 
    data.append({
        "author": author,
        "name": name,
        "part": part,
        "text": text
    })

# Save the result to a JSON file
import json
with open("life_and_times_baal_shem_tov_results.json", "w", encoding="utf-8") as outfile:
    json.dump(data, outfile, ensure_ascii=False, indent=4)
