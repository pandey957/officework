# -*- coding: utf-8 -*-
"""
Created on Tue Jun 14 15:59:33 2016

@author: sridhar.jeyaraman
"""

import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier

from sklearn import preprocessing
from sklearn.metrics import roc_curve, auc
number = preprocessing.LabelEncoder()

train=pd.read_csv('D:/Gender Identification Ext/outputTermMatrix40.csv')
#test1=pd.read_csv()

df_topic= pd.get_dummies(train['topic'])
train = pd.concat([train, df_topic], axis=1)


#Step-2: Convert categorical variable to numpy arrays and fill NaN values to zero.
def convert(data):
    number = preprocessing.LabelEncoder()
    data['gender'] = number.fit_transform(data.gender)
    data['age'] = number.fit_transform(data.age)
    data['topic'] = number.fit_transform(data.topic)
    data['star_sign'] = number.fit_transform(data.star_sign)
    data['date'] = number.fit_transform(data.date)
    data['post'] = number.fit_transform(data.post)
    data['abstractnoun'] = number.fit_transform(data.abstractnoun)
    data['adjall'] = number.fit_transform(data.adjall)
    data['adjpert'] = number.fit_transform(data.adjpert)
    data['adjppl'] = number.fit_transform(data.adjppl)
    data['advall'] = number.fit_transform(data.advall)
    data['article'] = number.fit_transform(data.article)
    data['basicprepositions'] = number.fit_transform(data.basicprepositions)
    data['causalwords'] = number.fit_transform(data.causalwords)
    data['causation'] = number.fit_transform(data.causation)
    data['certaintywords'] = number.fit_transform(data.certaintywords)
    data['change'] = number.fit_transform(data.change)
    data['cognitive'] = number.fit_transform(data.cognitive)
    data['communicationofideas'] = number.fit_transform(data.communicationofideas)
    data['conjunctions'] = number.fit_transform(data.conjunctions)
    data['constraining'] = number.fit_transform(data.constraining)
    data['determiners'] = number.fit_transform(data.determiners)
    data['dimensions'] = number.fit_transform(data.dimensions)
    data['exclusivewords'] = number.fit_transform(data.exclusivewords)
    data['existence'] = number.fit_transform(data.existence)
    data['fact'] = number.fit_transform(data.fact)
    data['familyreference'] = number.fit_transform(data.familyreference)
    data['form'] = number.fit_transform(data.form)
    data['formationofideas'] = number.fit_transform(data.formationofideas)
    data['functionalwords'] = number.fit_transform(data.functionalwords)
    data['hedgephrases'] = number.fit_transform(data.hedgephrases)
    data['individualvolition'] = number.fit_transform(data.individualvolition)
    data['inorganicmatter'] = number.fit_transform(data.inorganicmatter)
    data['intersocialvolitionsection'] = number.fit_transform(data.intersocialvolitionsection)
    data['iwords'] = number.fit_transform(data.iwords)
    data['litigious'] = number.fit_transform(data.litigious)
    data['moralaffections'] = number.fit_transform(data.moralaffections)
    data['motion'] = number.fit_transform(data.motion)
    data['negative'] = number.fit_transform(data.negative)
    data['negativemood'] = number.fit_transform(data.negativemood)
    data['negativetone'] = number.fit_transform(data.negativetone)
    data['neutraltone'] = number.fit_transform(data.neutraltone)
    data['nounact'] = number.fit_transform(data.nounact)
    data['nounanimal'] = number.fit_transform(data.nounanimal)
    data['nounartifact'] = number.fit_transform(data.nounartifact)
    data['nounattribute'] = number.fit_transform(data.nounattribute)
    data['nounbody'] = number.fit_transform(data.nounbody)
    data['nouncognition'] = number.fit_transform(data.nouncognition)
    data['nouncommunication'] = number.fit_transform(data.nouncommunication)
    data['nounevent'] = number.fit_transform(data.nounevent)
    data['nounfeeling'] = number.fit_transform(data.nounfeeling)
    data['nounfood'] = number.fit_transform(data.nounfood)
    data['noungroup'] = number.fit_transform(data.noungroup)
    data['nounlocation'] = number.fit_transform(data.nounlocation)
    data['nounmotive'] = number.fit_transform(data.nounmotive)
    data['nounobject'] = number.fit_transform(data.nounobject)
    data['nounperson'] = number.fit_transform(data.nounperson)
    data['nounphenomenon'] = number.fit_transform(data.nounphenomenon)
    data['nounplant'] = number.fit_transform(data.nounplant)
    data['nounpossession'] = number.fit_transform(data.nounpossession)
    data['nounprocess'] = number.fit_transform(data.nounprocess)
    data['nounquantity'] = number.fit_transform(data.nounquantity)
    data['nounrelation'] = number.fit_transform(data.nounrelation)
    data['nounshape'] = number.fit_transform(data.nounshape)
    data['nounstate'] = number.fit_transform(data.nounstate)
    data['nounsubstance'] = number.fit_transform(data.nounsubstance)
    data['nounsword'] = number.fit_transform(data.nounsword)
    data['nountime'] = number.fit_transform(data.nountime)
    data['nountops'] = number.fit_transform(data.nountops)
    data['number'] = number.fit_transform(data.number)
    data['order'] = number.fit_transform(data.order)
    data['organicmatter'] = number.fit_transform(data.organicmatter)
    data['other'] = number.fit_transform(data.other)
    data['personalaffections'] = number.fit_transform(data.personalaffections)
    data['positive'] = number.fit_transform(data.positive)
    data['positivemood'] = number.fit_transform(data.positivemood)
    data['positivetone'] = number.fit_transform(data.positivetone)
    data['preposition'] = number.fit_transform(data.preposition)
    data['prepositions'] = number.fit_transform(data.prepositions)
    data['pronouns'] = number.fit_transform(data.pronouns)
    data['quantity'] = number.fit_transform(data.quantity)
    data['relation'] = number.fit_transform(data.relation)
    data['religiousaffections'] = number.fit_transform(data.religiousaffections)
    data['social'] = number.fit_transform(data.social)
    data['soundadjectives'] = number.fit_transform(data.soundadjectives)
    data['spaceingeneral'] = number.fit_transform(data.spaceingeneral)
    data['stopwords'] = number.fit_transform(data.stopwords)
    data['superfluous'] = number.fit_transform(data.superfluous)
    data['sympatheticaffections'] = number.fit_transform(data.sympatheticaffections)
    data['time'] = number.fit_transform(data.time)
    data['uncertainty'] = number.fit_transform(data.uncertainty)
    data['verbbody'] = number.fit_transform(data.verbbody)
    data['verbchange'] = number.fit_transform(data.verbchange)
    data['verbcognition'] = number.fit_transform(data.verbcognition)
    data['verbcommunication'] = number.fit_transform(data.verbcommunication)
    data['verbcompetition'] = number.fit_transform(data.verbcompetition)
    data['verbconsumption'] = number.fit_transform(data.verbconsumption)
    data['verbcontact'] = number.fit_transform(data.verbcontact)
    data['verbcreation'] = number.fit_transform(data.verbcreation)
    data['verbemotion'] = number.fit_transform(data.verbemotion)
    data['verbmotion'] = number.fit_transform(data.verbmotion)
    data['verbperception'] = number.fit_transform(data.verbperception)
    data['verbpossession'] = number.fit_transform(data.verbpossession)
    data['verbsocial'] = number.fit_transform(data.verbsocial)
    data['verbstative'] = number.fit_transform(data.verbstative)
    data=data.fillna(0)
    return data

train=convert(train)

#For female

#Step-3: Split the data set to train and validate
train['is_train'] = np.random.uniform(0, 1, len(train)) <= .75
train, validate = train[train['is_train']==True], train[train['is_train']==False]

x_train = train[['abstractnoun','adjall','adjpert','adjppl','advall','article','basicprepositions','causalwords','causation','certaintywords','change','cognitive','communicationofideas','conjunctions','constraining','determiners','dimensions','exclusivewords','existence','fact','familyreference','form','formationofideas','functionalwords','hedgephrases','individualvolition','inorganicmatter','intersocialvolitionsection','iwords','litigious','moralaffections','motion','negative','negativemood','negativetone','neutraltone','nounact','nounanimal','nounartifact','nounattribute','nounbody','nouncognition','nouncommunication','nounevent','nounfeeling','nounfood','noungroup','nounlocation','nounmotive','nounobject','nounperson','nounphenomenon','nounplant','nounpossession','nounprocess','nounquantity','nounrelation','nounshape','nounstate','nounsubstance','nounsword','nountime','nountops','number','order','organicmatter','other','personalaffections','positive','positivemood','positivetone','preposition','prepositions','pronouns','quantity','relation','religiousaffections','social','soundadjectives','spaceingeneral','stopwords','superfluous','sympatheticaffections','time','uncertainty','verbbody','verbchange','verbcognition','verbcommunication','verbcompetition','verbconsumption','verbcontact','verbcreation','verbemotion','verbmotion','verbperception','verbpossession','verbsocial','verbstative','Accounting', 'Advertising', 'Agriculture', 'Architecture', 'Arts', 'Automotive', 'Banking', 'Biotech', 'BusinessServices', 'Chemicals', 'Communications-Media', 'Construction', 'Consulting', 'Education', 'Engineering', 'Environment', 'Fashion', 'Government', 'HumanResources', 'Internet', 'InvestmentBanking', 'Law', 'LawEnforcement-Security', 'Manufacturing', 'Marketing', 'Military', 'Museums-Libraries', 'Non-Profit', 'Publishing', 'RealEstate', 'Religion', 'Science', 'Sports-Recreation', 'Student', 'Technology', 'Telecommunications', 'Tourism', 'Transportation', 'indUnk']]
y_train = train['gender']

x_validate = validate[['abstractnoun','adjall','adjpert','adjppl','advall','article','basicprepositions','causalwords','causation','certaintywords','change','cognitive','communicationofideas','conjunctions','constraining','determiners','dimensions','exclusivewords','existence','fact','familyreference','form','formationofideas','functionalwords','hedgephrases','individualvolition','inorganicmatter','intersocialvolitionsection','iwords','litigious','moralaffections','motion','negative','negativemood','negativetone','neutraltone','nounact','nounanimal','nounartifact','nounattribute','nounbody','nouncognition','nouncommunication','nounevent','nounfeeling','nounfood','noungroup','nounlocation','nounmotive','nounobject','nounperson','nounphenomenon','nounplant','nounpossession','nounprocess','nounquantity','nounrelation','nounshape','nounstate','nounsubstance','nounsword','nountime','nountops','number','order','organicmatter','other','personalaffections','positive','positivemood','positivetone','preposition','prepositions','pronouns','quantity','relation','religiousaffections','social','soundadjectives','spaceingeneral','stopwords','superfluous','sympatheticaffections','time','uncertainty','verbbody','verbchange','verbcognition','verbcommunication','verbcompetition','verbconsumption','verbcontact','verbcreation','verbemotion','verbmotion','verbperception','verbpossession','verbsocial','verbstative','Accounting', 'Advertising', 'Agriculture', 'Architecture', 'Arts', 'Automotive', 'Banking', 'Biotech', 'BusinessServices', 'Chemicals', 'Communications-Media', 'Construction', 'Consulting', 'Education', 'Engineering', 'Environment', 'Fashion', 'Government', 'HumanResources', 'Internet', 'InvestmentBanking', 'Law', 'LawEnforcement-Security', 'Manufacturing', 'Marketing', 'Military', 'Museums-Libraries', 'Non-Profit', 'Publishing', 'RealEstate', 'Religion', 'Science', 'Sports-Recreation', 'Student', 'Technology', 'Telecommunications', 'Tourism', 'Transportation', 'indUnk']]
y_validate = validate['gender']

lg = LogisticRegression()
lg.fit(x_train, y_train)
Disbursed_lg=lg.predict_proba(x_validate)
fpr, tpr, _ = roc_curve(y_validate, Disbursed_lg[:,1])
roc_auc = auc(fpr, tpr)
print(roc_auc)
lg.score(x_validate, y_validate)

rf = RandomForestClassifier(n_estimators=830, criterion = 'entropy',max_features=None,n_jobs=-1,warm_start=True)
rf.fit(x_train, y_train)
disbursed = rf.predict_proba(x_validate)
fpr, tpr, _ = roc_curve(y_validate, disbursed[:,1])
roc_auc = auc(fpr, tpr)
print(roc_auc)
rf.score(x_validate, y_validate)


gb=GradientBoostingClassifier(learning_rate=0.205)
gb.fit(x_train,y_train)
Disbusedgb=gb.predict_proba(x_validate)
fpr,tpr,_=roc_curve(y_validate,Disbusedgb[:,1])
roc_auc=auc(fpr,tpr)
print(roc_auc)
gb.score(x_validate, y_validate)

kn=KNeighborsClassifier()
kn.fit(x_train,y_train)
Disbusedkn=kn.predict_proba(x_validate)
fpr,tpr,_=roc_curve(y_validate,Disbusedkn[:,1])
roc_auc=auc(fpr,tpr)
print(roc_auc)
kn.score(x_validate, y_validate)


dt=DecisionTreeClassifier(max_depth=6,max_features='log2')
dt.fit(x_train,y_train)
Disbuseddt=dt.predict_proba(x_validate)
fpr,tpr,_=roc_curve(y_validate,Disbuseddt[:,1])
roc_auc=auc(fpr,tpr)
print(roc_auc)
dt.score(x_validate, y_validate)



