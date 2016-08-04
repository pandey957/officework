import socket
import sys
import time
import csv
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('localhost',int(sys.argv[1])) 
sock.bind(server_address)
sock.listen(1)
print >>sys.stderr, 'waiting for a connection'
connection, client_address = sock.accept()
try:
  print >>sys.stderr, 'connection from', client_address
  file_in = open('time_series.csv')
  file_in.readline()
  for line in csv.reader(file_in):
    data = connection.send(line[0]+', ' + line[1]+'\n')
    time.sleep(0.25)
finally:
  connection.close()

