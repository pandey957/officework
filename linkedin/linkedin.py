from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from datetime import datetime
import time
import smtplib
import csv
count = True
print "Opening browser"
url = 'https://www.quora.com/What-are-the-things-that-only-Indians-say'
driver = webdriver.Chrome()
driver.get('https://in.linkedin.com/')
elem1 = driver.find_element_by_id('login-email')
elem1.send_keys('ashish.rajoriya3@gmail.com')
elem2 = driver.find_element_by_id('login-password')
elem2.send_keys('up85aq8490')
path1 = driver.find_element_by_xpath("//form[@action='https://www.linkedin.com/uas/login-submit']/input[6]")
path1.click()
#time.sleep(5)
driver.get('https://www.linkedin.com/vsearch/f?adv=true&trk=federated_advs')
driver.execute_script("document.getElementsByClassName('hidden')[2].className='countryCode'")
driver.execute_script("document.getElementsByClassName('hidden')[2].className='postalCode'")
driver.execute_script("$('#advs-countryCode').removeAttr('disabled')")
driver.execute_script("$('#advs-locationType')[0].value = 'I'")

in_file = open("input.csv")
in_file.readline()
reader = csv.reader(in_file)
for row in reader:
    print row[2]
    driver.execute_script("""
                          var foo = arguments[0];
                          $('#advs-firstName')[0].value = arguments[0];
                          $('#advs-lastName')[0].value = arguments[1];
                          $('#advs-postalCode')[0].value = arguments[2];
                          """,
                          row[2], row[1], row[7])
    time.sleep(1)
    driver.execute_script("document.getElementsByClassName('form-controls')[0].getElementsByTagName('input')[0].click()")
    time.sleep(1)
