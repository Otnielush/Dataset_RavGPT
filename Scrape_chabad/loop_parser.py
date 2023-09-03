import cloudscraper
import json
from bs4 import BeautifulSoup
import os
import pyperclip

# Create a cloudscraper instance
scraper = cloudscraper.create_scraper(delay=10, browser="chrome")
print("Scraper created")



base_url = 'https://www.chabad.org/library/article_cdo/aid/114871/jewish/Introduction.htm'


def get_link_book():
    data = {}
    print(f"Provide link pls:")
    data['base_url'] = input().strip()
    print("\tName of book:")
    data['name'] = input().strip()
    print("\tChapter of book (if need):")
    data['chapter'] = input().strip()
    print("\tAuthor:")
    data['author'] = input().strip()
    print("Fix?: (y / any)")
    data['fix'] = input().strip().lower() == 'y'

    # file name fix
    for invalid in [':', '*', '/', '"', '?', '>', '|', '<']:
        data['name'] = data['name'].replace(invalid, '')
    return data

def check_book_parsed(result_folder, name_of_book):
    path = os.path.join(result_folder, name_of_book + '.json')
    if os.path.isfile(path):
        return True
    return False

# Variables for the general details
author = "Jacob Immanuel Schochet"
name = "Lamplighters: The Philosophy of Lubavitch Activism"


if __name__ == '__main__':
    result_folder = "tmp_parsed"
    os.makedirs(result_folder, exist_ok=True)
    # main loop
    while True:
        params = {'fix': True}
        results = []

        while params['fix']:
            params = get_link_book()
            if check_book_parsed(result_folder, params['name']):
                print(f"Book already parsed!\nAdd to book? (y / any)")

                if input().strip().lower() == 'y':  # reading existing file
                    with open(f"{result_folder}/{params['name']}.json", 'r', encoding='utf-8') as f:
                        results = json.load(f)
                else:  # changing parsing data
                    params['fix'] = True


        # start parsing
        page_num = 1
        while params['base_url']:  # While there's a URL to process
            print(f'Parsing page: {page_num}', end="\r")

            response = scraper.get(params['base_url']).text
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
                params['base_url'] = "https://www.chabad.org" + next_page_anchor['href'] + "#lt=primary"  # english
            else:
                pyperclip.copy(params['base_url'])
                params['base_url'] = False  # No more pages to process

            # Organizing the data into a dictionary and appending to the results list
            data = {
                "author": params['author'],
                "name": params['name'],
                "chapter": params['chapter'],
                "part": part,
                "text": text
            }
            results.append(data)
            page_num += 1

        # Remove the last (empty) result if it's indeed empty
        if not results[-1]["text"]:
            results.pop()

        # Save results to a JSON file
        with open(f"{result_folder}/{params['name']}.json", 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=4)

        print(f"\n\nResults saved to {result_folder}/{params['name']}.json\nLast link copied to clipboard\n")

