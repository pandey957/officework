import requests
from requests import get, post, ConnectionError
import json
import re
from comment import Comment
from unicode import UnicodeWriter
import time
class Blog(object):
    """
    The Blog Class
    """
    def __init__(self, key, outfile, query, comments=False, match_mode='all',
                    body='full_text', filter_language='en', sort_mode='time_desc',
                    query_limit=10, blog_comments='off', filter_inserted_from = None,
                    filter_inserted_to = None):
        self.outfile = outfile
        self.url = 'http://api.boardreader.com/v1/Blogs/Search'
        self.filter_inserted_from = filter_inserted_to
        self.filter_inserted_to = filter_inserted_to
        self.key = key
        self.query = query
        self.match_mode = match_mode
        self.body = body
        self.blog_comments = blog_comments
        self.filter_language = filter_language
        self.sort_mode = sort_mode
        self.query_limit = query_limit
        self.header_written = False
        self.max_limit = 200
        self.response = self.get_response()
    def get_params(self):
        return {
            'key': self.key, 'query': self.query, 'match_mode': self.match_mode, 'body': self.body,
            'filter_language': self.filter_language, 'sort_mode': self.sort_mode, 'limit': min(self.query_limit,self.max_limit),
            'rt': 'json', 'blog_comments': self.blog_comments, 'filter_inserted_from': self.filter_inserted_from,
            'filter_inserted_to': self.filter_inserted_to }
    def get_response(self):
        """
        Involved in making request to api
        """
        response  = requests.get(self.url, self.get_params())
        if response.status_code != 200: raise ConnectionError('Got error other than %s', 200)
        response = response.json()['response']
        if response.has_key('Error'):
            raise ValueError('Invalid output: %', json.dumps(response['Error']))
        self.query_limit -= min(self.query_limit,self.max_limit)
        return response
    def total_found(self):
        return self.response['TotalFound']
    def save_response(self):
        while self.query_limit > 0:
            self.filter_inserted_to = int(time.mktime(time.strptime(self.response['Matches']['Match'][-1]['Published'],"%Y-%m-%d %H:%M:%S")))
            self.response['Matches']['Match'].extend(self.get_response()['Matches']['Match'])
        wrtr_file = open(self.outfile,'wb')
        wrtr = UnicodeWriter(wrtr_file)
        wrtr.writerow([u'Language', u'Url', u'Published', u'Country', u'ThreadId', u'Inserted', u'PostSize',
        u'Subject', u'Text'])
        for item in self.response['Matches']['Match']:
            text = re.sub('[\,\n\t\b-]','',item['Text'])
            text = text.replace(',','')
            wrtr.writerow([item[u'Language'], item[u'Url'], item[u'Published'], item['Country'],
                item[u'ThreadId'], item[u'Inserted'], str(item['PostSize']), item['Subject'].replace(',',''), text])
        wrtr_file.close()
        for item in self.response['Matches']['Match']:
            if item[u'CommentsInThread'] > 0:
                self.write_header_comment_file()
                Comment(key=self.key, outfile='comment_' + self.outfile, filter_thread = item[u'ThreadId'])
    def write_header_comment_file(self):
        if self.header_written: return
        comment_file = 'comment_' + self.outfile
        wrtr_file = open(comment_file,'ab')
        wrtr = UnicodeWriter(wrtr_file)
        wrtr.writerow([u'Language', u'Url', u'Published', u'Country', u'ThreadId', u'Inserted', u'PostSize',
        u'Subject', u'Text'])
        wrtr_file.close()
        self.header_written = True
