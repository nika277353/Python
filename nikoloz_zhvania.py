import requests
from bs4 import BeautifulSoup
import csv
import time


def fetch_page(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36',
        'Accept-Language': 'en-US,en;q=0.9',
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.content
    else:
        return None


def extract_titles(html):
    soup = BeautifulSoup(html, 'html.parser')
    titles = []
    h2_elements = soup.find_all('h2', class_='film-name')
    for h2 in h2_elements:
        title = h2.find('a').text.strip()
        titles.append(title)
    return titles


def main():
    base_url = 'https://dopebox.to/movie?page='
    page_number = 1
    titles = []

    while page_number <= 5:
        url = base_url + str(page_number)
        html = fetch_page(url)
        print(html)

        if html is not None:
            new_titles = extract_titles(html)
            titles.extend(new_titles)
            print(f'Page {page_number} processed.')
            page_number += 1
            time.sleep(1)
        else:
            print(f'Failed to fetch page {page_number}. Retrying in 5 seconds...')
            time.sleep(5)


    with open('titles.csv', 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Title'])
        for title in titles:
            writer.writerow([title])

    print('Titles saved to titles.csv.')


if __name__ == '__main__':
    main()
