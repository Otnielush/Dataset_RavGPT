import cloudscraper
from bs4 import BeautifulSoup
import json
scraper = cloudscraper.create_scraper(delay=10, browser="chrome")

base_url = 'https://www.chabad.org/library/article_cdo/aid/1208507/jewish/The-Baal-Shem-TovA-Brief-Biography.htm'
response = scraper.get(base_url).text
soup = BeautifulSoup(response, 'html.parser')
for tag in soup.find_all(class_="pullquote"):
    tag.decompose()


# Variables for the general details
author = "Peretz Golding"
name = "The Baal Shem Tov—A Brief Biography"
results = []


def clean_text(text):
    remove_strings = [
        "The resting place of Rabbi Yisroel in the town of Mezhibush, during the Communist Era.",
        "The town of Mezhibush, where Rabbi Yisroel resided, today.",
        "Rabbi Yisroel’s prayer book, found today at the Central Lubavitch Library, Agudas Chasidei Chabad."
    ]
    for string in remove_strings:
        text = text.replace(string, "")
    
    # Remove everything after "Works cited in this biography:"
    index = text.find("Works cited in this biography:")
    if index != -1:
        text = text[:index]
    
    # Remove excessive newline and carriage return characters
    text = text.replace("\n", " ").replace("\r", " ")
    text = ' '.join(text.split())  # replace multiple spaces with a single space
    
    return text.strip()

# Extracting parts and their corresponding texts
sections = soup.find_all("section")
for section in sections:
    header = section.find("h2")
    part = header.text if header else ""

    if part == "Passing and Succession":
        text = clean_text(section.get_text().replace(part, ""))
        data = {
            "author": author,
            "name": name,
            "part": part,
            "text": text
        }
        results.append(data)
        break

    text = clean_text(section.get_text().replace(part, ""))

    data = {
        "author": author,
        "name": name,
        "part": part,
        "text": text
    }
    results.append(data)



# Saving results to a JSON file
with open("The_Baal_Shem_Tov_A_Brief_Biography.json", "w", encoding="utf-8") as outfile:
    json.dump(results, outfile, ensure_ascii=False, indent=4)

print("Data extraction complete!")

