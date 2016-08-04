import pandas as pd
import numpy as np
import matplotlib.pylab as plt
from statsmodels.tsa.arima_model import ARIMA


dateparse = lambda dates: pd.datetime.strptime(dates, '%Y-%m-%d %H:%M:%S')
data = pd.read_csv('time_series.csv', parse_dates=['Time'], index_col='Time',date_parser=dateparse)
ts_CO = data['CO']
ts_CO_log = np.log(ts_CO)
i=0
model = ARIMA(ts_CO_log[i:i+100], order=(2, 1, 1))
results_ARIMA = model.fit(disp=-1)
forecast = results_ARIMA.predict(start = 100, end= 104, dynamic= True)
forecast = forecast.cumsum()
print forecast
forecast = forecast.cumsum()
print forecast
print ts_CO_log.ix[i+99]
predictions_ARIMA_log = pd.Series(ts_CO_log.ix[i+99], index=forecast.index)
print predictions_ARIMA_log
predictions_ARIMA_log = predictions_ARIMA_log.add(forecast,fill_value=0)
print predictions_ARIMA_log
predictions_ARIMA = np.exp(predictions_ARIMA_log)
print predictions_ARIMA
