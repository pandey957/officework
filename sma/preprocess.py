# -*- coding: utf-8 -*-
"""
Created on Thu Apr  7 18:19:41 2016

@author: prateek.kansal
"""

import re
import nltk
from stemming.porter2 import stem
from autocorrect import spell
import time
import pandas as pd
import string

lemmatizer = nltk.stem.WordNetLemmatizer()

###############################################################################
##########                    Text Preprocessing                     ##########
###############################################################################

"""
text                     :     input sentence
keyword                  :     keyword searched by user
hashtag_remove           :     (Twitter Specific) Removing hashtag if it contains searched keyword else removing hash sign only, default = False
at_usr_remove            :     (Twitter Specific) Removing User names from the tweets, default = False
remove_url               :     Removing URL's, default = False
replaceSpecialChars      :     Replacing all characters except letters and numbers with space, default = True
replaceNumbers           :     Replacing all numbers with space, default = True
convertToLowerCase       :     Converting all the letters to lower case, default = True
removeDefaultStopWords   :     Removing the default stopwords like is, am, are etc. from the text, default = True
removeGivenWords         :     Removing the given words in the word_list from the text, default = False
stemWords                :     Stemming the words to return root word, default = False
lemmatize                :     Lemmatizing the words to return root word, default = False
spellcorrect             :     Trying to correct the spelling of the words which are not present in the python dictionary, default = False
word_list                :     list of words for removal given apart from stopwords for 'removeGivenWords' argument
"""

def preprocesstext(text, keyword, hashtag_remove = False, at_usr_remove = False, remove_url = False, replaceSpecialChars = True,
                   replaceNumbers = True, convertToLowerCase = True, removeDefaultStopWords = True, removeGivenWords = False,
                   stemWords = False, lemmatize = False, spellcorrect = False, word_list = []):
    assert isinstance(hashtag_remove,bool)
    assert isinstance(at_usr_remove,bool)
    assert isinstance(replaceSpecialChars,bool)
    assert isinstance(replaceNumbers,bool)
    assert isinstance(convertToLowerCase,bool)
    assert isinstance(removeDefaultStopWords,bool)
    assert isinstance(removeGivenWords,bool)
    assert isinstance(stemWords,bool)
    assert isinstance(lemmatize,bool)
    assert isinstance(spellcorrect,bool)
    assert isinstance(word_list,list) | isinstance(word_list,str)
    if hashtag_remove:
       hashtag = re.findall(r'#([A-Za-z0-9]+)', text)
       if len(hashtag) != 0:
           for i in hashtag:
               rep = '#' + i
               if keyword in i:
                   text = text.replace(rep,' ')
               else:
                   text = text.replace(rep,i)
    if at_usr_remove:
       at_usr = re.findall('@[^\s]+', text)
       for i in at_usr:
           text = text.replace(i,'')
    if remove_url:
       text = re.sub(r'((www\.[^\s]+)|(https://[^\s]+))','',text)
       text = re.sub("http\S+", "", text)
       text = re.sub("https\S+", "", text)
    text = re.sub(r"[^a-zA-Z0-9\s%s]" % re.escape(string.punctuation)," ",text)         # removing characters other than punctuations, numbers and letters
    if replaceSpecialChars:
       text = re.sub(r"[^0-9A-Za-z']", " ", text)
    if replaceNumbers:
       text = re.sub(r"[0-9]", " ",text)
    text = re.sub(r'([[:alpha:]])\1+', r'\1\1',text)   # removing extra instances of characters with more than 2 consecutive occurances
    if convertToLowerCase:
       text = str(text).lower()
    if removeDefaultStopWords:
       stopwords = "(^|\\s)(" + '|'.join(nltk.corpus.stopwords.words('english')) + ")(\\s|$)"
       text = re.sub(stopwords, " ", str(text))
    if removeGivenWords and len(word_list) != 0:
       if type(word_list) == str:
           text = re.sub(word_list, " ", str(text))
       else:
           otherwords = "(^|\\s)(" + str('|'.join(word_list)) + ")(\\s|$)"
           text = re.sub(otherwords, " ", str(text))
    text = re.sub(r"\s+", " ", str(text))    # multiple whitespace characters collapsed to a single blank
    text = str(text).strip()
    if stemWords:
       text = " ".join([stem(y) for y in str(text).split() if y not in nltk.corpus.stopwords.words('english')])
    if lemmatize:
       text = " ".join([lemmatizer.lemmatize(y) for y in str(text).split() if y not in nltk.corpus.stopwords.words('english')])
    if spellcorrect:
       text = " ".join([spell(y) for y in str(text).split() if y not in nltk.corpus.stopwords.words('english')])
    return(text)


## Example  ##

data = pd.read_csv('test.csv')
start_time = time.time()
#data['processed_text'] = data.text.apply(preprocesstext)
data['processed_text'] = list(map(lambda x: preprocesstext(text = x, keyword = "airline", hashtag_remove = True, at_usr_remove = True, remove_url = True, replaceSpecialChars = True,
                   replaceNumbers = True, convertToLowerCase = True, removeDefaultStopWords = True, removeGivenWords = False,
                   stemWords = False, lemmatize = False, spellcorrect = False, word_list = []), data.text))
run_time = time.time() - start_time
print("Preprocessing Time: " + str(round(run_time,2)) + " Seconds")

new_df = data[["text","processed_text"]]
new_df.to_csv("test_output.csv",index = False)
