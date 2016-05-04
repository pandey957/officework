from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from datetime import datetime
import time
import smtplib
import codecs
file_count = 0
print "Opening browser"
driver = webdriver.Chrome()
for line in open('urls'):
    driver.get(line)
    filename = 'outEconomist' + str(file_count) + '.html'
    outfile = codecs.open(filename,'wb',encoding="utf-8")
    file_count += 1
    driver.delete_all_cookies()
    driver.execute_script("$.modal.close();")
    driver.execute_script("""
        var test = $('#simplemodal-container')[0];
        test.parentNode.removeChild(test);
        var test = $('#simplemodal-overlay')[0]
        test.parentNode.removeChild(test);
        var test = $('#ec-cookie-messages-container')[0];
        test.parentNode.removeChild(test);
        var test = $('#leaderboard')[0];
        test.parentNode.removeChild(test);""")
    content = driver.page_source
    outfile.write(content)
    outfile.close()
driver.close()
