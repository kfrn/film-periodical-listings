#!/usr/bin/env python3

import json
import requests
import re
from bs4 import BeautifulSoup

TOTAL_PAGES = 36
issue_data = []

def construct_url(number):
    return "http://repositori.filmoteca.cat/handle/11091/8833/discover?order=ASC&rpp=100&sort_by=dc.date.created_dt_sort&page=" + str(number) + "&group_by=none&etal=0"

def extract_data(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')

    item_metadata = soup.find_all(class_='item-metadata')

    for item in item_metadata:
        title = item.find(class_='Z3988').get_text()
        date_raw_html = item.find_all(class_='content')
        full_link = "http://repositori.filmoteca.cat" + item.find('a')['href']

        if len(date_raw_html) > 1:
            date = date_raw_html[1].get_text()
        else:
            date = ''

        data = {'title': title, 'link': full_link, 'date': date}
        # print("Issue data:", data)

        issue_data.append(data)

for num in range(1, TOTAL_PAGES + 1):
    url = construct_url(num)
    print("Scraping page", num, "of the results:")
    extract_data(url)

with open('publicacions.json', 'w') as outfile:
    json.dump(issue_data, outfile)
