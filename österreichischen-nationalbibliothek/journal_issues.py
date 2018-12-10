#!/usr/bin/env python3

import csv
import pdb
import requests
from bs4 import BeautifulSoup


def read_in_journal_data():
    volumes = []

    with open('yearly_volumes.csv', 'r') as csv_file:
        reader = csv.reader(csv_file, delimiter=',')
        next(reader)

        for row in reader:
            journal_data = {
                'title': row[0],
                'year': row[1],
                'url': row[2]
            }

            volumes.append(journal_data)

        csv_file.close()

    return volumes


def parse_issue_page(soup, volume):
    issue_section = soup.find_all('dl')

    issues = []

    for i in issue_section:
        issue_number = i.find('h2').get_text().replace('Heft ', '')
        href = i.find('a')['href']
        url = full_url(href)

        issue = issue_data(volume, url, issue=issue_number)

        issues.append(issue)

    return issues


def parse_calendar_page(soup, volume):
    issue_links = soup.find_all('a')

    issues = []

    for i in issue_links:
        date = i['title'].replace('.', '')
        url = full_url(i['href'])

        issue = issue_data(volume, url, date=date)
        issues.append(issue)

    return issues


def full_url(url):
    if 'cgi-content' in url:
        return 'http://anno.onb.ac.at/' + url[1:]
    else:
        return 'http://anno.onb.ac.at/cgi-content' + url[1:]


def issue_data(volume, url, issue=None, date=None):
    return {
        'title': volume['title'],
        'year': volume['year'],
        'issue': issue,
        'date': date,
        'url': url
    }


def parse_html(volume):
    page = requests.get(volume['url'])
    soup = BeautifulSoup(page.content, 'html.parser')

    issues = []

    issue_page = soup.find(class_='prevws')
    calendar_page = soup.find(class_='view-month')

    if issue_page:
        issues.append(parse_issue_page(issue_page, volume))
    elif calendar_page:
        issues.append(parse_calendar_page(calendar_page, volume))
    else:
        print('Neither issue nor calendar page!')

    return [i for sublist in issues for i in sublist]


def write_out_data(journal_issues):
    with open('journal_issues.csv', 'w') as outfile:
        fields = list(journal_issues[0].keys())

        writer = csv.DictWriter(outfile, fieldnames=fields)
        writer.writeheader()
        for row in journal_issues:
            writer.writerow(row)


def retrieve_issue_data():
    journal_yearly_volumes = read_in_journal_data()

    issue_data = []

    for j in journal_yearly_volumes:
        issues = parse_html(j)
        issue_data.append(issues)

    all_issues = [i for sublist in issue_data for i in sublist]

    write_out_data(all_issues)


retrieve_issue_data()
