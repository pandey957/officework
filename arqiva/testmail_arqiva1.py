import smtplib
from password import getmail_data, close_mail
import email.message
from bs4 import BeautifulSoup
from azure.storage.table import TableService, Entity
table_service = TableService(account_name='rsastoragewestus', account_key='PNaraccyQ7oFvN9oaifPk4fjG8/vN8U+v577zFG+5npVHGXWgbOlGamgBlNjbsZU3rs7Kd7+r/Hnbqbk2Rowqw==')
msg_data = BeautifulSoup(open('test.html'),'lxml')
from envelopes import Envelope
import smtplib
import time
def mail(subject,msg,sender='power.bi@annik.com',receiver='anil.jha@annik.com'):
  envelope = Envelope(
    from_addr = sender, 
    to_addr = receiver,
    subject = subject,
    html_body = msg)
  #envelope.send('smtp.office365.com', login=sender,password='asdlfkj', tls=True)
  envelope.send('smtp.annik.com')


def check_device_status(record):
    return_record = {}
    return_record['id'] = record.deviceid
    if record.status == '10010':
        return_record['type'] = 'Temperature'
        return_record['reason'] = 'current device temperature: %s which is not in permitted limit.' % record.temp
    elif record.status == '100010':
        return_record['type'] = 'Pressure'
        return_record['reason'] = 'current device pressure: %s which is not in permitted limit.' % record.pressure
    elif record.status == '110':
        return_record['type'] = 'I/O'
        return_record['reason'] = 'There may be an I/O error with sensor/device.'
    elif record.status == '1010':
        return_record['type'] = 'Humidity'
        return_record['reason'] = 'current device humidity is: %s which is not in permitted limit.' % record.humidity
    elif record.status == '1000010':
        return_record['type'] = 'Battery'
        return_record['reason'] = 'Sensor batter is low.'

    if return_record.has_key('type'): return return_record
    else: return None




sender = 'power.bi@annik.com'
#receiver = 'vishal.sharma@anniksystems.com'
receiver = 'dinesh.batra@annik.com'
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
        device_check = check_device_status(record)
        if device_check:
            send_mails.append(device_check)
        past_time = record.finishtransmissiontime
    if len(send_mails)<1:
        print 'looking for another batch of emails'
        continue
    print 'trying to login'
    #mail = getmail_data(sender)
    print 'successfully logged in'
    for record in send_mails:
        #deviceId = record.deviceid
        #device_temparature = int(record.temp)
        msg['Subject'] = 'Device: %s have exceeded parameter limit' % record['id']
        print 'Trying to send mail'
        msg_data = BeautifulSoup(open('test.html'),'lxml')
        msg_data.find('emp').replaceWith(record['reason'])
        msg.set_payload(str(msg_data))
        mail(msg['subject'],str(msg_data),msg['From'], msg['To'])
        print 'sent mail for 1 record', time.ctime()
