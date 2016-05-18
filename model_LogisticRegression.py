import numpy as np
import pandas as pd
import scipy as sp
from sklearn.cross_validation import train_test_split
from sklearn import metrics
from sklearn.linear_model import LogisticRegression

final_col=['msisdn', 'stat_month', 'hm_prov', 'flag', 'vstd_prov_cont', 'rm_days', 'workday_days', 'holiday_days', 'specialday_days', 'workday_cont', 'holiday_cont', 'specialday_cont', 'workday_dr', 'holiday_dr', 'specialday_dr', 'call_cont', 'call_dr', 'avg_day_cont_totle', 'avg_day_dr_totle', 'avg_day_cont_workday', 'avg_day_dr_workday', 'avg_day_cont_holiday', 'avg_day_dr_holiday']
#linux data directory:
#data_201601= pd.read_csv('/mnt/shared/data_final_201601_balanced.csv',sep=',',header=0,names=final_col,index_col=['stat_month','msisdn','hm_prov'])
data_201601= pd.read_csv('E:/Clean Data/data_final_201601_origin.csv',sep=',',header=0,names=final_col,index_col=['stat_month','msisdn','hm_prov'])
# tmp=data_201601.pop('flag')
# data_201601.insert(0,'flag',tmp)

# origin data verify
# data_201601_org= pd.read_csv('E:/Clean Data/data_final_201601_origin.csv',sep=',',header=0,names=final_col,index_col=['stat_month','msisdn','hm_prov'])
# tmp=data_201601_org.pop('flag')
# data_201601_org.insert(0,'flag',tmp)
# X_org = data_201601_org.iloc[:,1:20]
# y_org = data_201601_org.iloc[:,0]
# predicted= model.predict(X_org)
# print(metrics.classification_report(y_org, predicted))
# print(metrics.confusion_matrix(y_org, predicted))
#logistic regression

X = data_201601.iloc[:,1:20]
y = data_201601.iloc[:,0]
# model.fit(X,y)
# predicted = model.predict(X)
# print(metrics.classification_report(y, predicted))
# print(metrics.confusion_matrix(y, predicted))
# verified model with origin data
# data_201601_test= pd.read_csv('E:/Clean Data/data_final_201601_origin.csv',sep=',',header=0,names=final_col,index_col=['stat_month','msisdn','hm_prov'])

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.30,random_state=100)
model = LogisticRegression()
model.fit(X_train,y_train)
predicted = model.predict(X_train)
print(metrics.classification_report(y_train, predicted))
print(metrics.confusion_matrix(y_train, predicted))
#fiting with other conf
predicted = model.predict(X_test)
print(metrics.classification_report(y_test, predicted))
print(metrics.confusion_matrix(y_test, predicted))

probas_=model.predict_proba(X_test)
pd.DataFrame(probas_[:,1],index=y_test.index,columns=['prob'])
