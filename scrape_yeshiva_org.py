import requests
from bs4 import BeautifulSoup
import json
import os

def extract_question_data(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Initialize data with default values
    data = {
        "jewish_date": "",
        "author": "",
        "question_type": "",
        "question_summary": "",
        "question": "",
        "answer": ""
    }

    try:
        # Extracting the required fields
        data["jewish_date"] = soup.find('h5', {'class': 'head-4'}).text.strip()
        data["author"] = soup.find('h3', {'class': 'head-3'}).text.strip()
        question_type_elements = soup.find('ul', {'class': 'flex'}).find_all('li')
        data["question_type"] = " ; ".join([ele.text.replace("keyboard_arrow_left", "").strip() for ele in question_type_elements])
        data["question_summary"] = soup.find('h1', {'class': 'head-2'}).text.strip()
        data["question"] = soup.find('div', {'id': 'questionText'}).text.strip()
        data["answer"] = soup.find('div', {'id': 'answerText'}).text.strip()
    except AttributeError as e:
        pass
    
    return data

results = []
LAST_PAGE=139500
PAGES_PER_FILE = 1500

for page_num in range(1, LAST_PAGE):  
    url = f'https://www.yeshiva.org.il/ask/{page_num}'
    results.append(extract_question_data(url))
    if page_num % PAGES_PER_FILE == 0 or page_num == LAST_PAGE:

        start_page = page_num - PAGES_PER_FILE + 1 if page_num != LAST_PAGE else page_num - (page_num % PAGES_PER_FILE) + 1

        filename = f'results_{start_page}_{page_num}.json'
        print(filename)
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=4)
        results = []  # Clear results for the next batch