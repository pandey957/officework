import requests
from requests import get, post, ConnectionError
import json
import re
from unicode import UnicodeWriter
class Comment(object):
    def __init__(self, key, outfile, filter_thread):
        self.url = 'http://api.boardreader.com/v1/Blogs/Thread'
        self.key = key
        self.outfile = outfile
        self.filter_thread = filter_thread
        self.response  = requests.get(self.url, {'key': self.key, 'rt': 'json', 'filter_thread' :self.filter_thread})
        wrtr_file = open(self.outfile,'ab')
        wrtr = UnicodeWriter(wrtr_file)
        for item in self.response.json()['response']['Matches']['Match']:
            text = re.sub('[\,\n\t\b-]','',item['Text'])
            text = text.replace(',','')
            wrtr.writerow([item[u'Language'], item[u'Url'], item[u'Published'], item['Country'],
                item[u'ThreadId'], item[u'Inserted'], str(item['PostSize']), item['Subject'].replace(',',''), text])
        wrtr_file.close()

    def test(self):
        return 'asfljf'
