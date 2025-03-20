# -*- coding: utf-8 -*-
"""
Created on Wed May 29 10:07:07 2024

@author: HW-T06
"""

import requests
from bs4 import BeautifulSoup
import time
import argparse

def fetch_ptt_titles(title):
    url = f'https://www.ptt.cc/bbs/{title}/index.html'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    cookies = {'over18': '1'}

    response = requests.get(url, headers=headers, cookies=cookies)
    soup = BeautifulSoup(response.text, 'html.parser')

    titles_data = []

    articles = soup.find_all('div', class_='r-ent')
    for article in articles:
        title_data = {}
        
        # Extract the push tag
        push_tag = article.find('div', class_='nrec').text.strip()
        title_data['push_tag'] = push_tag if push_tag else '0'

        # Extract the title
        title = article.find('div', class_='title').text.strip()
        title_data['title'] = title

        titles_data.append(title_data)

    return titles_data



def main():
    
        
    parser = argparse.ArgumentParser(description='Fetch ptt Title')
    parser.add_argument('title', type=str, help='title')
    args = parser.parse_args()

    
    titles = fetch_ptt_titles(args.title)
    print(f"PTT {args.title} Titles and Push-Tags:")
    for title in titles:
        print(f"{title['push_tag']}: {title['title']}")
    print("\n---\n")
    
        
    # while True:
    #     titles = fetch_ptt_titles(args.title)
    #     print(f"PTT {args.title} Titles and Push-Tags:")
    #     for title in titles:
    #         print(f"{title['push_tag']}: {title['title']}")
    #     print("\n---\n")
    #     time.sleep(30)  # Wait for 1 minute before updating again

if __name__ == '__main__':
    main()