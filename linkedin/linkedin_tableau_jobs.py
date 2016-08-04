from bs4 import BeautifulSoup
from unicodewriter import UnicodeWriter
from urllib import urlopen, urlencode
import csv
outfile = open('linkedin_job_companyname.csv','w')
out_wrtr = UnicodeWriter(outfile)
out_wrtr.writerow(['title','company','location','description'])
url = 'https://www.linkedin.com/jobs/search?keywords=Tableau&locationId=us:0&orig=JSERP&count=50&'
#https://www.linkedin.com/jobs/search?keywords=Tableau&locationId=us:0&orig=JSERP&start=0&count=50
data = {}
for i in range(25):
    data['start'] = i*50
    data_url = url + urlencode(data)
    soup = BeautifulSoup(urlopen(data_url),'lxml')
    for item in soup.findAll('li','job-listing'):
        title = item.find('span','job-title-text').text
        company = item.find('span','company-name-text').text
        location = item.find('span','job-location').find('span').text
        description = item.find('div','job-description').text
        print 'Running: ' + str(i*50) + ' page.'
        print '#'.join([title, company, location, description])
        print '\n'
        out_wrtr.writerow([title, company, location, description])
outfile.close()
