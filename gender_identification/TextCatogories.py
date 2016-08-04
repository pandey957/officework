import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.tokenize import RegexpTokenizer
import re
import time

start_time=time.clock()

infile = pd.DataFrame.from_csv('D:/Gender Identification Ext/GenderSample40K ADD.csv', sep=',')
dictGen = pd.DataFrame.from_csv('D:/Gender Identification Ext/fdict.csv',encoding = 'iso8859_16')

gender_dict = dictGen.set_index('id')['value'].to_dict()

tokenizer=RegexpTokenizer(r'\w+')
infile['post'] = infile['post'].str.lower()

def funMono(arg1):
    termm = tokenizer.tokenize(arg1)
    return ' '.join(map(lambda x: gender_dict.get(x,''),termm))
    
def funBi(arg1):
    termb = re.findall(r"\b\w+\s\w+", arg1)
    return ' '.join(map(lambda x: gender_dict.get(x,''),termb))

def funTri(arg1):
    termt = re.findall(r"\b\w+\s\w+\s\w+", arg1)
    return ' '.join(map(lambda x: gender_dict.get(x,''),termt))

def funTetra(arg1):
    termte = re.findall(r"\b\w+\s\w+\s\w+\s\w+", arg1)
    return ' '.join(map(lambda x: gender_dict.get(x,''),termte))

infile['monogram'] = infile['post'].apply(funMono)
infile['bigram'] = infile['post'].apply(funBi)
infile['Trigram'] = infile['post'].apply(funTri)
infile['Tetragram'] = infile['post'].apply(funTetra)

infile['Doctagger'] = infile.monogram.str.cat(others=[infile.bigram, infile.Trigram, infile.Tetragram], sep=' ')
infile['Doctagger'] = infile['Doctagger'].str.replace('\s+', ' ')
infile['Doctagger'] = infile['Doctagger'].str.replace('^\s+', '')

######BIGRAM Vectorization
bigram_vectorizer = TfidfVectorizer(ngram_range=(1,1), token_pattern=r'\b\w+\b', min_df=1)
bi_analyze = bigram_vectorizer.build_analyzer()

bi_XArray = bigram_vectorizer.fit_transform(infile['Doctagger']).toarray()
df2 = pd.DataFrame(bi_XArray,columns = bigram_vectorizer.get_feature_names(), index = infile.index)
bi_inputDTM = pd.concat([infile['gender'], infile['age'], infile['topic'], infile['star_sign'], infile['date'], infile['post'], df2], axis=1)
bi_inputDTM.to_csv('D:/Gender Identification Ext/outputTermMatrix40.csv')
print(time.clock()-start_time,":In Seconds")
