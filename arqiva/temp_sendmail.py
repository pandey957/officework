import smtplib
from password import *
import email.message
from bs4 import BeautifulSoup
from azure.storage.table import TableService, Entity
table_service = TableService(account_name='rsastoragewestus', account_key='PNaraccyQ7oFvN9oaifPk4fjG8/vN8U+v577zFG+5npVHGXWgbOlGamgBlNjbsZU3rs7Kd7+r/Hnbqbk2Rowqw==')
msg_data = BeautifulSoup(open('test.html'),'lxml')
sender = 'satyendra.pandey@anniksystems.com'
receiver = sender
msg = email.message.Message()
msg['Subject'] = 'Temparature exceed limit by %0.2f' % 30
msg['From'] = sender
msg['To'] = receiver
msg.add_header('Content-Type','text/html')
past_time = 0
while True:
    test = "finishtransmissiontime gt %d" % past_time
    print test
    tasks = table_service.query_entities('StreamOutputTable1', filter=test)
    if len(tasks)<1:
        print 'continuing loop'
        continue
    print 'trying to login'
    #mail = smtplib.SMTP('smtp.office365.com',587)
    #mail.ehlo()
    #mail.starttls()
    #mail.login(sender,token.decode('base64'))
    print 'successfully logged in'
    print 'length of records found:', str(len(tasks))
    for record in tasks:
        device_temparature = float(record.temp)
        print 'checking for temperature'
        if device_temparature <= 30:
            print 'temperarture is less than limit'
            past_time = record.finishtransmissiontime
            continue
        deviceId = record.deviceid
        device_temparature = int(record.temp)
        print 'Trying to send mail'
        msg_data = BeautifulSoup(open('test.html'),'lxml')
        msg_data.find('emp').replaceWith(deviceId)
        msg.set_payload(str(msg_data))
        mail.sendmail(msg['From'], [msg['To']], msg.as_string())
        print 'sent mail for 1 record'
        past_time = record.finishtransmissiontime
    mail.quit()
    mail.close()
