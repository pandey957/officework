import smtplib
from password import getmail_data, close_mail
import email.message
from bs4 import BeautifulSoup
from azure.storage.table import TableService, Entity
table_service = TableService(account_name='rsastoragewestus', account_key='PNaraccyQ7oFvN9oaifPk4fjG8/vN8U+v577zFG+5npVHGXWgbOlGamgBlNjbsZU3rs7Kd7+r/Hnbqbk2Rowqw==')
msg_data = BeautifulSoup(open('test.html'),'lxml')
def check_device_status(record):
    return_record = []
    return_record.append(record.deviceId)


sender = 'satyendra.pandey@anniksystems.com'
#receiver = 'vishal.sharma@anniksystems.com'
receiver = 'niraj.khalpada@anniksystems.com'
msg = email.message.Message()
msg['From'] = sender
msg['To'] = receiver
msg.add_header('Content-Type','text/html')
past_time = 0
while True:
    test = "finishtransmissiontime gt %d" % past_time
    #print test
    tasks = table_service.query_entities('StreamOutputTable1', filter=test)
    if len(tasks)<1: continue
    print 'length of records found:', str(len(tasks))
    send_mails = []
    for record in tasks:
        device_temparature = float(record.temp)
        if device_temparature > 30:
            send_mails.append(record)
        past_time = record.finishtransmissiontime
    if len(send_mails)<1:
        print 'looking for another batch of emails'
        continue
    print 'trying to login'
    mail = getmail_data(sender)
    print 'successfully logged in'
    for record in send_mails:
        deviceId = record.deviceid
        device_temparature = int(record.temp)
        msg['Subject'] = 'Temparature limit for device: %s ' % deviceId
        print 'Trying to send mail'
        msg_data = BeautifulSoup(open('test.html'),'lxml')
        msg_data.find('emp').replaceWith(deviceId)
        msg.set_payload(str(msg_data))
        mail.sendmail(msg['From'], [msg['To']], msg.as_string())
        print 'sent mail for 1 record'
    close_mail(mail)
