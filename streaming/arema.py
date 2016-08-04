import pandas as pd
import numpy as np
import matplotlib.pylab as plt
from statsmodels.tsa.arima_model import ARIMA
 
 
dateparse = lambda dates: pd.datetime.strptime(dates, '%Y-%m-%d %H:%M:%S')
data = pd.read_csv('time_series.csv', parse_dates=['Time'], index_col='Time',date_parser=dateparse)
#print (data.head(
#data.index
ts_CO = data['CO']
#ts_CO.head(10)
#ts_CO['1970-04-01 09:09:00']
ts_CO_log = np.log(ts_CO)
#ts_log_diff = ts_CO_log - ts_CO_log.shift()
#ts_log_diff.dropna(inplace=True)
i=0
while (i<16):
    model = ARIMA(ts_CO_log[i:i+100], order=(2, 1, 1))
    results_ARIMA = model.fit(disp=-1) 
    forecast = results_ARIMA.predict(start = 100, end= 104, dynamic= True)
    forecast = forecast.cumsum()
    predictions_ARIMA_log = pd.Series(ts_CO_log.ix[i+100], index=forecast.index)
    predictions_ARIMA_log = predictions_ARIMA_log.add(forecast,fill_value=0)
    predictions_ARIMA = np.exp(predictions_ARIMA_log)
    predictions_ARIMA.head()
    print predictions_ARIMA
    i = i+4
