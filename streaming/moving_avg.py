import socket
import time
import sys
from collections import deque
class movingAverage():
  def __init__(self, t_window):
    self.t_window = t_window
    self.stream = [0] * t_window
    self.avg = [0] * t_window
    self.rmse = [0] * t_window
  def addStream(self,items):
    if len(self.stream) >= self.t_window:  self.stream.pop(0)
    self.stream.append(items)
    self.avg1 = self.calAvg(1)
    self.avg2 = self.calAvg(2)
    if len(self.avg) >= self.t_window: self.avg.pop(0)
    self.avg.append(self.avg1)
    if len(self.rmse) >= self.t_window : self.rmse.pop(0)
    self.rmse.append((self.stream[-1] - self.avg[-2])**2)
    
  def calAvg(self,next=1):
    first_avg = sum(self.stream)/self.t_window
    if next==1: return first_avg
    else: return ( sum(self.stream) + first_avg - self.stream[0]) / self.t_window
  def re_dequ(self):
    return self.stream

  def calRmse(self): return sum(self.rmse)/self.t_window

if __name__ == '__main__':
  sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  server_address = ('localhost', int(sys.argv[1]))
  print >>sys.stderr, 'connecting to %s port %s' % server_address
  ma = movingAverage(int(sys.argv[2]))
  sock.connect(server_address)
  while True:
    data = sock.recv(100)
    ma.addStream(float(data.split(', ')[-1]))
    print data.strip() + '\t' +  str(ma.avg1) + '\t' + str(ma.avg2) + '\t' +  str(ma.calRmse())

