from pyspark.sql import Row
file = sc.textFile('/spark-data/input/cf/output.csv')
Record = Row('customer_id','product_id','sale_dt','invoice_id','units')
data = file.map(lambda x: Record(*x.split(',')))
data = sqlContext.createDataFrame(data)
sqlContext.registerDataFrameAsTable(data,'table1')
df = sqlContext.sql('select customer_id, product_id, count(invoice_id) as prod_in_transactions from table1 group by customer_id, product_id')
df.write.format('json').save(/spark-data/input/cf/output)
df = sqlContext.read.load("/spark-data/input/cf/output", format="json")


from pyspark.sql import Row
from pyspark.sql.types import *
file = sc.textFile('/spark-data/input/cf/output.csv')
def extract_data(data):
    data = data.split(',')
    r_data = [data[0],data[1],data[-1]]
    r_data = [int(r.replace('"','')) for r in r_data]
    return r_data
data = file.map(extract_data)
schema = StructType([ StructField('customer_id',IntegerType(),True), StructField('product_id',IntegerType(),True),StructField('units',IntegerType(),True)])
df = sqlContext.createDataFrame(data,schema=schema)
sqlContext.registerDataFrameAsTable(df,'table2')
df = sqlContext.sql('select customer_id, product_id, sum(units) as units from table2 group by customer_id, product_id')
df.map(lambda x: ','.join([str(r) for r in x])).saveAsTextFile('/spark-data/input/cf/output_units')

sc= SparkContext(appName="expedia1")
from pyspark import Row
train = sc.textFile("/spark-data/input/train.csv")
header = train.first()
Person = Row(*header.split(','))
train = train.filter(lambda x: x != header).map(lambda x: Person(*x.split(',')))
df_train = sqlContext.createDataFrame(train)
destinations = sc.textFile("/spark-data/input/destinations.csv")
header_des = destinations.first()
Person1 = Row(*header_des.split(','))
destination = destinations.filter(lambda x: x!=header_des).map(lambda x: Person1(*x.split(',')))
df_destination = sqlContext.createDataFrame(destination)
df_output = df_train.join(df_destination,df_train.srch_destination_id == df_destination.srch_destination_id,'left')
df_output.map(lambda x: ',',join([str(r) for r in x])).saveAsTextFile('/spark-data/ouput/expedia_merged')
sc.stop()

from pyspark.sql.types import *
in_file = sc.textFile('file:///home/reco1/data/prod_sales/ProductSales_20130404.csv')
def oritentData(record):
    record = record.split(',')
    indexes = [1,2,7,11,5,8,20]
    return [ record[i].replace('"','') for i in indexes]

def filterData(record):
    flag = True
    if (int(record[3])<1 == flag) or (record[5] not in (['1','4'])) or (record[-1] != ''): flag = False
    return flag

data = in_file.map(oritentData).filter(filterData).map(lambda x: [int(i) for i in x[:-3]])
schema = StructType([ StructField('customer_id',IntegerType(),True), StructField('product_id',IntegerType(),True),StructField('invoice_id',IntegerType(),True),StructField('units',IntegerType(),True)])
df = sqlContext.createDataFrame(data,schema)
sqlContext.registerDataFrameAsTable(df,'table1')
df_instances = sqlContext.sql('select customer_id, product_id, count(invoice_id) as prod_in_transactions from table1 group by customer_id, product_id')
df_instances.map(lambda x: ','.join([str(r) for r in x])).saveAsTextFile('/user/reco1/data/algoinput/instances')
df_units = sqlContext.sql('select customer_id, product_id, sum(units) as units from table1 group by customer_id, product_id')
df_units.map(lambda x: ','.join([str(r) for r in x])).saveAsTextFile('/user/reco1/data/algoinput/units')

def oritentData(record):
  record = record.split(',')
  indexes = [1,2,7,11,5,8,20]
  return [ record[i].replace('"','') for i in indexes]

def filterData(record):
  flag = True
  if (int(record[-4])<1) or (record[-2] not in (['1','4'])) or (record[-1] != ''): flag = False
  return flag

from pyspark.sql import Row
file = sc.textFile('/user/reco1/data/staging/*.csv')
data = file.map(oritentData).filter(filterData).map(lambda x: [i for i in x[:-3]])
Record = Row('customer_id','product_id','invoice_id','units')
data = data.map(lambda x: Record(*x))
data = sqlContext.createDataFrame(data)
sqlContext.registerDataFrameAsTable(data,'table1')
df = sqlContext.sql('select customer_id, product_id, count(invoice_id) as prod_in_transactions from table1 group by customer_id, product_id')
df.map(lambda x: ','.join([str(r) for r in x])).saveAsTextFile('/spark-data/output/testing')



from pyspark.sql.types import *
from pyspark.sql import Row
from pyspark import SQLContext
from pyspark
import sys
def oritentData(record):
  record = record.split(',')
  indexes = [1,2,7,11,5,8,20]
  return [ record[i].replace('"','') for i in indexes]

def filterData(record):
  flag = True
  if (int(record[-4])<1) or (record[-2] not in (['1','4'])) or (record[-1] != ''): flag = False
  return flag


in_file = sc.textFile('/user/reco1/data/staging/*.csv')
data = in_file.map(oritentData).filter(filterData).map(lambda x: [i for i in x[:-3]])
Record = Row('customer_id','product_id','invoice_id','units')
data = data.map(lambda x: Record(*x))
data = sqlContext.createDataFrame(data)
sqlContext.registerDataFrameAsTable(data,'table1')
df = sqlContext.sql('select customer_id, product_id, count(invoice_id) as prod_in_transactions from table1 group by customer_id, product_id')
df.map(lambda x: ','.join([str(r) for r in x])).saveAsTextFile(sys.argv[2])



from envelopes import Envelope
import smtplib

envelope = Envelope(
    from_addr = 'anil.jha@annik.com',
    to_addr = 'pandey957@gmail.com',
    subject = 'Hello',
    text_body = 'Hello')

envelope.send('172.16.8.28')




from pyspark.sql.types import *
from pyspark.sql import Row
from pyspark import SparkContext
from pyspark import SQLContext
import sys
def oritentData(record):
  record = record.split(',')
  indexes = [1,2,7,11,5,8,20]
  return [ record[i].replace('"','') for i in indexes]

def filterData(record):
  flag = True
  if (int(record[-4])<1) or (record[-2] not in (['1','4'])) or (record[-1] != ''): flag = False
  return flag

if __name__ == '__main__':
  sc = SparkContext(appName = 'CF_prod_in_transaction')
  sqlContext = SQLContext(sc)
  in_file = sc.textFile(sys.argv[1])
  data = in_file.map(oritentData).filter(filterData).map(lambda x: [int(i) for i in x[:-3]])
  Record = Row('customer_id','product_id','invoice_id','units')
  data = data.map(lambda x: Record(*x))
  data = sqlContext.createDataFrame(data)
  sqlContext.registerDataFrameAsTable(data,'table1')
  df = sqlContext.sql('select customer_id, product_id, sum(units) as prod_in_transactions from table1 group by customer_id, product_id')
  df.map(lambda x: ','.join([str(r) for r in x])).saveAsTextFile(sys.argv[2])
  sc.stop()



data_path,header,train_sample,number,support,confidence,lift,k,testing,testing_split,seed,output_path
write = open('test.csv','w')
wrtr = csv.writer(write)

import csv
read = open('arqiva.csv')
for line in read: wrtr.writerow(line)

from e
envelope = Envelope(
    from_addr = 'satyendra.pandey@annik.com',
    to_addr = 'satyendra.pandey@annik.com',
    subject = 'Hello',
    text_body = 'Hello')
