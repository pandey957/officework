
import csv
import oauth2 as oauth
import urllib2 as urllib
import json
import sys
from unicodewriter import UnicodeWriter
api_key = "Q0517YMBvBv0F3gL8kRFMVRqw"
api_secret = "G7xOg3x5nbaspDQM7qy9eBqiOJbxoNEDdgkW60I2RtO2TZP0YR"
access_token_key = "113656956-PmS2sHEh46CeVPWty8kuWYfkgjf4LBluvxaM9fHb"
access_token_secret = "qH6xmqiVYrPV6Q38DDDUwQVUyuXT0UEgVB83RTIgTAU8a"
outputfile = open('outputfile.csv','wb')
count = 0
#sys.stdout = outputfile
wttr = UnicodeWriter(outputfile)
_debug = 0
oauth_token    = oauth.Token(key=access_token_key, secret=access_token_secret)
oauth_consumer = oauth.Consumer(key=api_key, secret=api_secret)
signature_method_hmac_sha1 = oauth.SignatureMethod_HMAC_SHA1()
http_method = "GET"
http_handler  = urllib.HTTPHandler(debuglevel=_debug)
https_handler = urllib.HTTPSHandler(debuglevel=_debug)

'''
Construct, sign, and open a twitter request
using the hard-coded credentials above.
'''
def twitterreq(url, method, parameters):
  req = oauth.Request.from_consumer_and_token(oauth_consumer,
                                             token=oauth_token,
                                             http_method=http_method,
                                             http_url=url,
                                             parameters=parameters)
  req.sign_request(signature_method_hmac_sha1, oauth_consumer, oauth_token)
  headers = req.to_header()
  encoded_post_data = None
  url = req.to_url()
  opener = urllib.OpenerDirector()
  opener.add_handler(http_handler)
  opener.add_handler(https_handler)
  response = opener.open(url, encoded_post_data)
  return response


def fetchsamples(max_id = None):
  keys1 = [u'contributors', u'truncated', u'text', u'is_quote_status', u'in_reply_to_status_id', u'id', u'favorite_count', u'entities', u'retweeted', u'coordinates', u'source', u'in_reply_to_screen_name', u'in_reply_to_user_id', u'retweet_count', u'id_str', u'favorited', u'user', u'geo', u'in_reply_to_user_id_str', u'lang', u'created_at', u'in_reply_to_status_id_str', u'place', u'metadata']
  #url = "https://api.twitter.com/1.1/statuses/home_timeline.json"
  global count
  url = 'https://api.twitter.com/1.1/search/tweets.json'
  parameters = {'q':'#JNURow','count':100}
  if max_id: parameters['max_id'] = max_id
  response = twitterreq(url, "GET", parameters)
  response = json.load(response)
  row = list()
  for attr in response['statuses']:
    print [attr[index] for index in keys1]
    #print attr['text'], ',', attr['created_at']
    count += 1
    max_id = attr['id']
  print "########################## read:", count, "Tweets"
  fetchsamples(max_id)

if __name__ == '__main__':
  fetchsamples()
