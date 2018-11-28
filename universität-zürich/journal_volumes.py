#!/usr/bin/env python3

import csv
import requests
import re
from bs4 import BeautifulSoup

JOURNAL_LINKS = [
    'https://www.e-periodica.ch/digbib/volumes?UID=kin-001',
    'https://www.e-periodica.ch/digbib/volumes?UID=ifz-001',
    'https://www.e-periodica.ch/digbib/volumes?UID=ifz-002',
    'https://www.e-periodica.ch/digbib/volumes?UID=ifz-003',
    'https://www.e-periodica.ch/digbib/volumes?UID=eil-001',
    'https://www.e-periodica.ch/digbib/volumes?UID=kif-001',
    'https://www.e-periodica.ch/digbib/volumes?UID=kif-002'
]


volume_data = []


def retrieve_journal_volume_data(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')

    title = soup.find(class_='page-content').find('h2').get_text()
    volumes_html = soup.find_all(class_='volume-thumbnail')

    for v in volumes_html:
        basic_data = extract_basic_data(v, title)
        volume_data.append(basic_data)


def extract_basic_data(html, title):
    url = html.find('a')['href']
    caption = html.find(class_='volume-caption').get_text()
    year = re.search(r'\d{4}', caption).group()
    volume_text = re.search(r'Volume \d{0,3}', caption).group()
    volume = volume_text.replace('Volume ', '')

    return {'title': title, 'volume': volume, 'year': year, 'url': url}


def write_out_data(journal_volumes):
    with open('journal_volumes.csv', 'w') as outfile:
        fields = list(journal_volumes[0].keys())

        writer = csv.DictWriter(outfile, fieldnames=fields)
        writer.writeheader()
        for row in journal_volumes:
            writer.writerow(row)


for journal in JOURNAL_LINKS:
    retrieve_journal_volume_data(journal)
    write_out_data(volume_data)
