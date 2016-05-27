from pyspark.sql import Row
file = sc.textFile('/spark-data/input/cf/output.csv')
Record = Row('customer_id','product_id','sale_dt','invoice_id','units')
data = file.map(lambda x: Record(*x.split(',')))
data = sqlContext.createDataFrame(data)
sqlContext.registerDataFrameAsTable(data,'table1')
df = sqlContext.sql('select customer_id, product_id, count(invoice_id) as prod_in_transactions from table1 group by customer_id, product_id')
df.write.format('json').save(/spark-data/input/cf/output)
df = sqlContext.read.load("/spark-data/input/cf/output", format="json")
