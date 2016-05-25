import numpy as np
import pandas as pd
import scipy as sp
final_col=['msisdn', 'stat_month', 'hm_prov', 'flag', 'vstd_prov_cont', 'rm_days', 'workday_days', 'holiday_days', 'specialday_days', 'workday_cont', 'holiday_cont', 'specialday_cont', 'workday_dr', 'holiday_dr', 'specialday_dr', 'call_cont', 'call_dr', 'avg_day_cont_totle', 'avg_day_dr_totle', 'avg_day_cont_workday', 'avg_day_dr_workday', 'avg_day_cont_holiday', 'avg_day_dr_holiday']


data_201601= pd.read_csv('E:/Clean Data/data_final_201601_origin.csv',sep=',',header=0,names=final_col,index_col=['stat_month','msisdn','hm_prov'])

#understanding datas
data_201601.corr()
data_201601[data_201601['flag']==1].describe()
plt.boxplot(data_201601[data_201601['call_count']<data_201601['call_count'].quantile(0.95)]['call_count'])
plt.hist(data_201601[data_201601['call_count']<data_201601['call_count'].quantile(0.95)]['call_count'])

#PCA
from sklearn.decomposition import PCA
pca = PCA(n_components=5,copy=False,whiten=True)
pca.fit(X)
X_pca=pca.fit_transform(X)

#data set split

X = data_201601.iloc[:,1:20]
y = data_201601.iloc[:,0]

from sklearn.cross_validation import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.30,random_state=100)

from sklearn.linear_model import LogisticRegression
model = LogisticRegression()
model.fit(X_train,y_train)
predicted = model.predict(X_train)

from sklearn import metrics
print(metrics.classification_report(y_train, predicted))
print(metrics.confusion_matrix(y_train, predicted))

predicted = model.predict(X_test)
print(metrics.classification_report(y_test, predicted))
print(metrics.confusion_matrix(y_test, predicted))

#random forest
from sklearn.ensemble import RandomForestClassifier
model= RandomForestClassifier(n_estimators=100)
model.fit(X_train, y_train)
predicted = model.predict(X_train)
print(metrics.classification_report(y_train, predicted))
print(metrics.confusion_matrix(y_train, predicted))

predicted = model.predict(X_test)
print(metrics.classification_report(y_test, predicted))
print(metrics.confusion_matrix(y_test, predicted))
