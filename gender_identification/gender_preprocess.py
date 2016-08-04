# -*- coding: utf-8 -*-
"""
Created on Wed Mar 09 13:17:46 2016

@author: sridhar.jeyaraman
"""
import pandas as pd
import numpy as np
import re
import os

def fun1(maledf1,staging,femaledf1,part=1):
    temp_male = maledf1[(part-1)*len(maledf1)/24:part*len(maledf1)/24]
    temp_female = femaledf1[(part-1)*len(femaledf1)/24:part*len(femaledf1)/24]
    temp = temp_male.append(temp_female)
    temp.to_csv(os.path.join(staging,str(part)+'.csv'),sep='\t')

#Special Charter removal#
def preprocess(in_file,staging):
    df1=pd.DataFrame.from_csv(in_file, sep='\t')
    df1['post'] = df1['post'].str.lower()
    df1['post'] = df1['post'].str.replace('urllink', '')
    df1['post'] = df1['post'].str.replace('http:\/\/.*[\r\n]*', '')
    df1['post'] = df1['post'].str.replace('(', '')
    df1['post'] = df1['post'].str.replace(')', '')
    df1['post'] = df1['post'].str.replace('@', '')
    df1['post'] = df1['post'].str.replace('#', '')
    df1['post'] = df1['post'].str.replace('-', '')
    df1['post'] = df1['post'].str.replace('*', '')
    df1['post'] = df1['post'].str.replace('^', '')
    df1['post'] = df1['post'].str.replace("'and'nbsp;", '')
    df1['post'] = df1['post'].str.replace('[', '')
    df1['post'] = df1['post'].str.replace(']', '')
    df1['post'] = df1['post'].str.replace('{', '')
    df1['post'] = df1['post'].str.replace('}', '')
    df1['post'] = df1['post'].str.replace('<', '')
    df1['post'] = df1['post'].str.replace('>', '')
    df1['post'] = df1['post'].str.replace('\s+', ' ')
    df1['post'] = df1['post'].str.replace('~', '')
    df1["post"] = [re.sub(r'\.\.+', '',str(i)) for i in df1["post"]]
    df1["post"] = [re.sub(r'"', '',str(i)) for i in df1["post"]]
    df1["post"] = [re.sub(r'|', '',str(i)) for i in df1["post"]]
    df1["post"] = [re.sub(r'!', '',str(i)) for i in df1["post"]]
    df1["post"] = [re.sub(r',', '',str(i)) for i in df1["post"]]
    df1['post'] = df1['post'].str.strip()
    df1=df1[df1.post<>'']
    np.random.seed(1000)
    maledf1=df1[df1.gender=='male']
    maledf1 = maledf1.iloc[np.random.permutation(len(maledf1))]
    femaledf1=df1[df1.gender=='female']
    femaledf1 = femaledf1.iloc[np.random.permutation(len(femaledf1))]
    for i in xrange(1,25):
        fun1(maledf1,femaledf1,i)
        print "create the Gender Sample " + str(i)
