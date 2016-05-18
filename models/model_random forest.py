import numpy as np
import pandas as pd
import scipy as sp
from sklearn.cross_validation import train_test_split
#use RandomForestRegressor for regression problem
from sklearn.ensemble import RandomForestClassifier 
from sklearn import metrics
final_col=['msisdn', 'stat_month', 'hm_prov', 'flag', 'vstd_prov_cont', 'rm_days', 'workday_days', 'holiday_days', 'specialday_days', 'workday_cont', 'holiday_cont', 'specialday_cont', 'workday_dr', 'holiday_dr', 'specialday_dr', 'call_cont', 'call_dr', 'avg_day_cont_totle', 'avg_day_dr_totle', 'avg_day_cont_workday', 'avg_day_dr_workday', 'avg_day_cont_holiday', 'avg_day_dr_holiday']
#linux data directory:
#data_201601= pd.read_csv('/mnt/shared/data_final_201601_balanced.csv',sep=',',header=0,names=final_col,index_col=['stat_month','msisdn','hm_prov'])
data_201601= pd.read_csv('E:/Clean Data/data_final_201601_balanced.csv',sep=',',header=0,names=final_col,index_col=['stat_month','msisdn','hm_prov'])

# origin data verify
# data_201601_org= pd.read_csv('E:/Clean Data/data_final_201601_origin.csv',sep=',',header=0,names=final_col,index_col=['stat_month','msisdn','hm_prov'])
# X_org = data_201601_org.iloc[:,1:20]
# y_org = data_201601_org.iloc[:,0]
# predicted= model.predict(X_org)
# print(metrics.classification_report(y_org, predicted))
# print(metrics.confusion_matrix(y_org, predicted))

X = data_201601.iloc[:,1:20]
y = data_201601.iloc[:,0]
#data reshape done!
# PCA proccess
# from sklearn.decomposition import PCA
# pca = PCA(n_components=5,copy=False,whiten=True)
# pca.fit(X)
# X_pca=pca.fit_transform(X)
#split dataset into train set(train model) and test set(validate model)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.30,random_state=100)
#Assumed you have, X (predictor) and Y (target) for training data set and x_test(predictor) of test_dataset
# Create Random Forest object
model= RandomForestClassifier(n_estimators=501)
# Train the model using the training sets and check score
model.fit(X_train, y_train)
predicted= model.predict(X_train)
print(metrics.classification_report(y_train, predicted))
print(metrics.confusion_matrix(y_train, predicted))
#Predict text set Output
predicted= model.predict(X_test)
print(metrics.classification_report(y_test, predicted))
print(metrics.confusion_matrix(y_test, predicted))
#feature_importances evaluate
feature_importances=pd.DataFrame(model.feature_importances_,index=X.columns)

# predict probablity
probas_=model.predict_proba(X_test)
prob=pd.DataFrame(probas_[:,1],index=y_test.index,columns=['prob'])
pd.concat([y_test,prob],axis=1)

