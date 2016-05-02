from urllib import urlopen, urlencode
from bs4 import BeautifulSoup
import csv
import re
import time
from difflib import SequenceMatcher as sm
cutoffAddressMatch = 0.8
addr_match_out = 'full_address_match_'
no_addr_match_out = 'no_address_match_'
last_name_match_addr = 'last_name_match_address'
no_last_name_match_addr = 'no_last_name_match_address'
curr_time = time.strftime("%Y%m%d%H%M%S")

def mergeLocality(addressLocality, addressRegion, postalCode):
    return addressLocality + ', ' + addressRegion + ' ' + postalCode

def createWriter(filename):
    fileHandler = open(filename+curr_time+'.csv','wb')
    return csv.writer(fileHandler,delimiter=',')

def writerHeader(wrtr):
    wrtr.writerow(['ARRELSETID', 'Name','streetAddress','addressRegion','phone','gender'])

def getwriterObj():
    wrtr_addr_match = createWriter(addr_match_out)
    wrtr_no_addr_match = createWriter(no_addr_match_out)
    wrtr_ln_match_addr = createWriter(last_name_match_addr)
    wrtr_no_ln_match_addr = createWriter(no_last_name_match_addr)
    return (wrtr_addr_match, wrtr_no_addr_match, wrtr_ln_match_addr, wrtr_no_ln_match_addr)
