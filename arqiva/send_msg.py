log_date=`date +"%Y%m%d%H%M%S"`
filename=`echo $0 | cut -d'.' -f1`

spark_log_warn=$log_path$filename'_warn_'$log_date.log
spark_log_error=$log_path$filename'_error_'$log_date.log

#job_done_file=$0_complete

files=`hdfs dfs -ls /user/reco1/data/staging | wc -l`

if [ $files -gt 3 ]; then
  file_to_remove=`hdfs dfs -ls /user/reco1/data/staging | sort -k 6,7 | head -2 | tail -1 | cut -d" " -f11`
  hdfs dfs -rm $file_to_remove 2> $spark_log_warn >> $spark_log_error
fi

hdfs dfs -put $in_unix_files_path/*.csv $in_hdfs_data_path/ 2> $spark_log_warn >> $spark_log_error

# [ -f $job_done_file ] && rm $job_done_file

python job_started.py $filename

hdfs dfs -test -d $out_hdfs_data_path

if [ $? -eq 0 ]; then
  hdfs dfs -rm -r $out_hdfs_data_path 2> $spark_log_warn  >> $spark_log_error
fi
spark-submit --master yarn --deploy-mode cluster $1 $in_hdfs_data_path/*.csv  $out_hdfs_data_path 2> $spark_log_warn  >> $spark_log_error

if [ $? -ne 0 ]; then
  python job_failed.py $filename $spark_log_warn $spark_log_error
else
  python job_complete.py $filename
  touch $job_done_file
  rm $in_unix_files_path/*
fi

---------------------------------------
file_check=/home/reco1/data/prod_sales/start_job_complete
if [ ! -f $file_check ];then
exit
fi
sh run_mba_date_view_pyspark.sh mba_date_view.py

from envelopes import Envelope
import smtplib
envelope = Envelope(
    from_addr = 'satyendra.pandey@annik.com',
    to_addr = 'satyendra.pandey@annik.com',
    subject = 'subject',
    text_body = 'sdfasf')
envelope.send('172.16.8.28')
#envelope.send('172.16.8.28', login='power.bi@annik.com',password='Annik#123', tls=True)



from clockwork import clockwork
api = clockwork.API('2bba3f5cb100cb0b3e1085c6b546a1ffe2f2cec8')
message = clockwork.SMS(to = '9910055945', message = 'This is a test message.')
response = api.send(message)


----------------------------
from pyspark.mllib.fpm import FPGrowth
from pyspark.mllib.evaluation import RankingMetrics
from pyspark import SparkContext
#sc = SparkContext(appName='aslkjsdf')
data = sc.textFile('/spark-data/input/eval_100000')
header = data.first()
data1 = data.filter( lambda x: x != header)
data = data1.map(lambda x: x.split(",")).map( lambda x: tuple([x[2],x[0]])).distinct()
data = data.groupByKey().mapValues(list).map(lambda x : x[1])
data.saveAsTextFile('/spark-data/testing/formatted_data')
train,test = data.randomSplit([7, 3], 0)
model = FPGrowth.train(data, minSupport=0.01)
result = model.freqItemsets()
result.saveAsTextFile('/spark-data/testing/ouput/complete')
