#!/usr/bin/env python3

import csv
import re
import requests
from bs4 import BeautifulSoup


def read_in_journal_volume_data():
    journal_volume_data = []

    with open('journal_volumes.csv', 'r') as csv_file:
        reader = csv.reader(csv_file, delimiter=',')
        next(reader)

        for row in reader:
            volume_data = {
                'title': row[0],
                'volume': row[1],
                'year': row[2],
                'url': row[3]
            }

            journal_volume_data.append(volume_data)

        csv_file.close()

    return journal_volume_data


def get_request(url):
    # NOTE: without full headers, the full HTML was not being returned.

    cookies = {'JSESSIONID': '5B15CAF3F951CD14372311AEA27E75DB'}
    headers = {
        'Connection': 'keep-alive',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Referer': 'https://www.e-periodica.ch/digbib/volumes?UID=kin-001',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
    }

    return requests.get(url, headers=headers, cookies=cookies)


def parse_html(volume):
    page = get_request(volume['url'])
    soup = BeautifulSoup(page.content, 'html.parser')

    issues = []
    issues_html = soup.find_all(class_='hierarchy-20')

    for i in issues_html:
        issue_number = i.find('a').get_text()
        issue_numeral = issue_number.replace('Issue ', '')
        url = i.find('a')['href']

        issue = {
            'title': volume['title'],
            'volume': volume['volume'],
            'issue': issue_numeral,
            'year': volume['year'],
            'url': url
        }
        print(issue)

        issues.append(issue)

    return issues


def write_out_data(journal_issues):
    with open('journal_issues.csv', 'w') as outfile:
        fields = list(journal_issues[0].keys())

        writer = csv.DictWriter(outfile, fieldnames=fields)
        writer.writeheader()
        for row in journal_issues:
            writer.writerow(row)


def retrieve_issue_data():
    volumes = read_in_journal_volume_data()
    issue_data = []

    for volume in volumes:
        issues = parse_html(volume)
        issue_data.append(issues)

    all_issues = [i for sublist in issue_data for i in sublist]
    print(f'{len(all_issues)} issues found!')

    write_out_data(all_issues)


retrieve_issue_data()
