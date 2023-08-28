import cloudscraper
import json
from bs4 import BeautifulSoup

# Create a cloudscraper instance
scraper = cloudscraper.create_scraper(delay=10, browser="chrome")
print("Scraper created")

base_url = 'https://www.chabad.org/library/article_cdo/aid/115020/jewish/The-Dilemma.htm'

# Variables for the general details
author = "Jacob Immanuel Schochet"
name = "Lamplighters: The Philosophy of Lubavitch Activism"
results = []

while base_url:  # While there's a URL to process
    response = scraper.get(base_url).text
    soup = BeautifulSoup(response, 'html.parser')

    # Extracting the required fields
    part_header = soup.find("h1", {"class": "article-header__title js-article-title js-page-title"})
    if part_header:
        part = part_header.text.strip()
    else:
        part = None

    text_div = soup.find("div", {"class": "co_body article-body cf"})
    if text_div:
        text_parts = text_div.find_all("p")
        text = "\n".join([p.get_text() for p in text_parts])
    else:
        text = None

    next_page_anchor = soup.find("a", {"class": "next_article"})
    if next_page_anchor:
        # Construct the full URL for the next page
        base_url = "https://www.chabad.org" + next_page_anchor['href']
    else:
        base_url = None  # No more pages to process

    # Organizing the data into a dictionary and appending to the results list
    data = {
        "author": author,
        "name": name,
        "part": part,          
        "text": text
    }
    results.append(data)

# Remove the last (empty) result if it's indeed empty
if not results[-1]["text"]:
    results.pop()

# Save results to a JSON file
with open('Religious_Duty_and_Religious_Experience_in_Chassidism.json', 'w', encoding='utf-8') as f:
    json.dump(results, f, ensure_ascii=False, indent=4)

print("Results saved to results.json")