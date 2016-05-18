import numpy as np
import pandas as pd
import scipy as sp
from sklearn import metrics
from sklearn import svm
from sklearn.cross_validation import train_test_split
#data reshape
final_col=['msisdn', 'stat_month', 'hm_prov', 'flag', 'vstd_prov_cont', 'rm_days', 'workday_days', 'holiday_days', 'specialday_days', 'workday_cont', 'holiday_cont', 'specialday_cont', 'workday_dr', 'holiday_dr', 'specialday_dr', 'call_cont', 'call_dr', 'avg_day_cont_totle', 'avg_day_dr_totle', 'avg_day_cont_workday', 'avg_day_dr_workday', 'avg_day_cont_holiday', 'avg_day_dr_holiday']
#data_201601= pd.read_csv('/mnt/shared/data_final_201601.csv',sep=',',header=0,names=final_col,index_col=['stat_month','msisdn','hm_prov'])
data_201601= pd.read_csv('E:/Clean Data/data_final_201601_balanced.csv',sep=',',header=0,names=final_col,index_col=['stat_month','msisdn','hm_prov'])
X = data_201601.iloc[:,1:20]
y = data_201601.iloc[:,0]
#data reshape done!
#SVM
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.70,random_state=100)
model = svm.SVC(cache_size=1000)
model.fit(X_train, y_train)
#Predict text set Output
predicted= model.predict(X_test)
print(metrics.classification_report(y_test, predicted))
print(metrics.confusion_matrix(y_test, predicted))