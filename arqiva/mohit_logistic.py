from math import exp
import sys
import time
from pyspark import SparkContext
from pyspark.mllib.classification import LogisticRegressionWithSGD
from pyspark.mllib.regression import LabeledPoint
from numpy import array
def parsePoint(line):
  values = [float(x) for x in line.split('\t')]
  out_var = values[-1]
  if out_var == 2: out_var = 0
  return LabeledPoint(out_var, values[:-1])

data.map(parsePoint).first()
#sc = SparkContext(appName="PythonLR")
# start timing
start = time.time()
data = sc.textFile("file:///root/GoodbadData")
parsedData = data.map(parsePoint)
model = LogisticRegressionWithSGD.train(parsedData)
testdata = sc.textFile("sWSpark_test.csv")
parsedTestData = testdata.map(parsePoint)
# Evaluating the model on test data
labelsAndPreds = parsedTestData.map(lambda p: (p.label, model.predict(p.features)))
trainErr = labelsAndPreds.filter(lambda (v, p): v != p).count() / float(parsedData.count())
print("Training Error = " + str(trainErr))
end = time.time()
print("Time is = " + str(end - start))
