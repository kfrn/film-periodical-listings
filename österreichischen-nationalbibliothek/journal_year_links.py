#!/usr/bin/env python3

import csv
import pdb
import requests
from bs4 import BeautifulSoup


def read_in_journal_data():
    journals = []

    with open('silent-era_journals.csv', 'r') as csv_file:
        reader = csv.reader(csv_file, delimiter=',')
        next(reader)

        for row in reader:
            journal_data = {
                'title': row[0],
                'years': row[1],
                'url': row[3]
            }

            journals.append(journal_data)

        csv_file.close()

    return journals


def parse_year_links(soup, title):
    volumes_html = soup.find(class_='view-year')
    years = volumes_html.find_all('a')

    volumes = []

    for y in years:
        volume = {
            'title': title,
            'year': y.get_text(),
            'url': f"http://anno.onb.ac.at{y['href']}"
        }
        volumes.append(volume)

    return volumes


def parse_html(journal):
    page = requests.get(journal['url'])
    soup = BeautifulSoup(page.content, 'html.parser')

    return parse_year_links(soup, journal['title'])


def write_out_data(yearly_volumes):
    with open('yearly_volumes.csv', 'w') as outfile:
        fields = list(yearly_volumes[0].keys())

        writer = csv.DictWriter(outfile, fieldnames=fields)
        writer.writeheader()
        for row in yearly_volumes:
            writer.writerow(row)


def retrieve_yearly_data():
    journals = read_in_journal_data()

    yearly_volumes = []

    for j in journals:
        volumes = parse_html(j)
        yearly_volumes.append(volumes)

    all_yearly_volumes = [i for sublist in yearly_volumes for i in sublist]

    write_out_data(all_yearly_volumes)


retrieve_yearly_data()
