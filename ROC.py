import numpy as np
import pandas as pd
import scipy as sp
from sklearn.cross_validation import train_test_split
from sklearn import metrics
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_curve, auc
final_col=['stat_month','msisdn','hm_prov','vstd_prov_count','rm_days','workday_days','holiday_days','specialday_days','workday_count','holiday_count','specialday_count','workday_dur','holiday_dur','specialday_dur','flag','call_count','call_dur','avg_day_count_totle','avg_day_dur_totle','avg_day_count_workday','avg_day_dur_workday','avg_day_count_holiday','avg_day_dur_holiday']
data_201601= pd.read_csv('E:/Clean Data/data_final_201601_balanced.csv',sep=',',header=0,names=final_col,index_col=['stat_month','msisdn','hm_prov'])
X = data_201601.iloc[:,1:20]
y = data_201601.iloc[:,0]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.30,random_state=100)
model = LogisticRegression()
model.fit(X_train,y_train)


# roc curve
probas_ = model.fit(X_train,y_train).predict_proba(X_test)
mean_tpr = 0.0
mean_fpr = np.linspace(0, 1, 100)
fpr, tpr, thresholds = roc_curve(y_test, probas_[:, 1])
mean_tpr += interp(mean_fpr, fpr, tpr)
mean_tpr[0] = 0.0 
roc_auc = auc(fpr, tpr)
plt.plot(fpr, tpr, lw=1, label='area = %0.2f' % ( roc_auc))