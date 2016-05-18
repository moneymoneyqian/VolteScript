import numpy as np
import pandas as pd
import scipy as sp

final_col=['msisdn', 'stat_month', 'hm_prov', 'flag', 'vstd_prov_cont', 'rm_days', 'workday_days', 'holiday_days', 'specialday_days', 'workday_cont', 'holiday_cont', 'specialday_cont', 'workday_dr', 'holiday_dr', 'specialday_dr', 'call_cont', 'call_dr', 'avg_day_cont_totle', 'avg_day_dr_totle', 'avg_day_cont_workday', 'avg_day_dr_workday', 'avg_day_cont_holiday', 'avg_day_dr_holiday']
#data_201601= pd.read_csv('/mnt/shared/data_final_201601.csv',sep=',',header=0,names=final_col,index_col=['stat_month','msisdn','hm_prov'])
data_201601= pd.read_csv('E:/Clean Data/data_final_201601_balanced.csv',sep=',',header=0,names=final_col,index_col=['stat_month','msisdn','hm_prov'])
tmp=data_201601.pop('flag')
data_201601.insert(0,'flag',tmp)
#data reshape done!
X = data_201601.iloc[:,1:20]
y = data_201601.iloc[:,0]

from sklearn.decomposition import PCA
pca = PCA(n_components=5,copy=False,whiten=True)
pca.fit(X)
new=pca.fit_transform(X)
from sklearn import metrics
from sklearn.linear_model import LogisticRegression
model = LogisticRegression()
model.fit(new,y)
predicted = model.predict(new)
print(metrics.classification_report(y, predicted))
print(metrics.confusion_matrix(y, predicted))

from sklearn.cross_validation import train_test_split
from sklearn.ensemble import RandomForestClassifier #use RandomForestRegressor for regression problem
#Assumed you have, X (predictor) and Y (target) for training data set and x_test(predictor) of test_dataset
# Create Random Forest object
model= RandomForestClassifier(n_estimators=100)
# Train the model using the training sets and check score
model.fit(X, y)
#Predict Output
predicted= model.predict(X)
print(metrics.classification_report(y, predicted))
print(metrics.confusion_matrix(y, predicted))
feature_importances=np.DataFrame(model.feature_importances_,index=X.columns)