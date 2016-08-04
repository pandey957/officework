import socket
import time
import sys
from collections import deque
import pandas as pd
import numpy as np
from statsmodels.tsa.arima_model import ARIMA
class contDataFrame():  
  def __init__(self,t_window):
    self.df = pd.Series()
    self.t_window = t_window

  def addRecord(self,key,value):
    data = {pd.datetime.strptime(key,'%Y-%m-%d %H:%M:%S'): {'value': float(value)}}
    s1 = np.log(pd.DataFrame.from_dict(data,orient='index')['value'])
    self.df = self.df.append(s1)
    if len(self.df) > self.t_window : self.df = self.df[-self.t_window:]
  
  def fit(self):
    if len(self.df) < self.t_window: return None
    model = ARIMA(self.df, order=(2, 1, 1))
    results_ARIMA = model.fit(disp=-1)
    forecast = results_ARIMA.predict(start = self.t_window, end= self.t_window+2, dynamic= True)
    forecast = forecast.cumsum()
    predictions_ARIMA_log = pd.Series(self.df.ix[self.t_window-1], index=forecast.index)
    predictions_ARIMA_log = predictions_ARIMA_log.add(forecast,fill_value=0)
    predictions_ARIMA = np.exp(predictions_ARIMA_log)
    #print self.df
    return predictions_ARIMA

   

if __name__ == '__main__':
  sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  server_address = ('localhost', int(sys.argv[1]))
  print >>sys.stderr, 'connecting to %s port %s' % server_address
  ma = contDataFrame(int(sys.argv[2]))
  sock.connect(server_address)
  while True:
    data = sock.recv(100).strip()
    ma.addRecord(*data.split(', '))
    print data 
    print '#######################OUTPUT##########################'
    print ma.fit()
    
