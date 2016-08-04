from bs4 import BeautifulSoup
from urllib import urlopen
from unicodewriter import *
import csv
def get_result(base_url, page = None):
    if page: url = base_url + '_'  +  str(page)
    else:
        url = base_url
        page = 0
    print url
    data = BeautifulSoup(urlopen(url),'lxml')
    for item in data.find('ol','list-group unstyled').findAll('li','list-item'):
        info = item.find('div','item-info')
        name = item.find('h3').text
        segments = item.find('div','list-tags').text
        phone_html = info.find('b','contact-number')
        phone = ''
        if phone_html:
            phone =  phone_html.text
        address = info.find('address').text
        wrtr.writerow([name, segments, phone, address])
    pager = data.find('ul','pager').find('li','next')
    if pager:
        page += 1
        get_result(base_url, page)

if __name__ == '__main__':
    outfile = open('output.csv','wb')
    wrtr = UnicodeWriter(outfile)
    url = 'http://yellowpages.sulekha.com/mobile-phone-sales_mumbai'
    get_result(url)
    outfile.close()
