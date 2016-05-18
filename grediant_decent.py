import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

X = pd.read_csv('E:/sample/5.1.logistic_x.txt',sep=',',header=None,names=('v1','v2'))
y = pd.read_csv('E:/sample/5.1.logistic_y.txt',sep=',',header=None,names=('y'))











X=np.array(X)
plt.scatter(X[:,0], X[:,1], c=np.array(y), cmap=plt.cm.Paired)
xx = np.linspace(0, 10,100)
yy = -model.coef_[:,0]/model.coef_[:,1]*xx-model.intercept_
plt.plot(xx,yy,'k-')