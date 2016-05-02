from bs4 import BeautifulSoup
import csv
from urllib import urlopen

def repeat_task(base_url , extend_url, return_set):
    new_url = base_url + extend_url
    new_data = BeautifulSoup(urlopen(new_url),'html.parser')
    for line in new_data.findAll('div','searchResultPremier'):
        return_set.add(line.find('a')['href'])
    for line in new_data.findAll('div','searchResult'):
        return_set.add(line.find('a')['href'])
    next_page = new_data.find('span','wb-page-right')
    if next_page:
        next_page_url = next_page.find('a')
        if next_page_url:
            repeat_task(base_url, next_page_url['href'], return_set)
    return return_set

base_url = 'http://www.whitebook.co.uk'
url = 'http://www.whitebook.co.uk/directory/directoryservices/'
url_links = BeautifulSoup(urlopen(url),'html.parser')
for link in url_links.findAll('a','catList'):

    extend_url = link['href']
    new_url = base_url + extend_url
    output = set()
    links = repeat_task(base_url , extend_url, output)
    print 'got links successfully'
    for line in links:
        data = BeautifulSoup(urlopen(line),'html.parser')
        contact_details = data.findAll('td','listDetails1')
        details = []
        for detail in contact_details:
            details.append(detail.text.strip())
        print ', '.join(details)
    break
