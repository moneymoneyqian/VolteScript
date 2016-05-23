import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

X = pd.read_csv('E:/sample/5.1.logistic_x.txt',sep=',',header=None,names=('v1','v2'))
y = pd.read_csv('E:/sample/5.1.logistic_y.txt',sep=',',header=None,names=('y'))


#use sklearn to fit model
from sklearn.linear_model import LogisticRegression
model = LogisticRegression(solver='newton-cg')
model.fit(X,y)

# grediant decent to find best theta
def gradient_decent(X,y,theta,step=0.0001):
	X=pd.DataFrame(X)
	ones=pd.Series(np.ones(X.shape[0]))
	X=np.array(pd.concat([ones,X],axis=1))
	y=np.array(y)
	m=X.shape[0]
	for i in range(theta.size):
		sumpart=sumhx(X,y,i,theta)
		theta[i]=theta[i]-step*1/m*sumpart
	return theta

def logit(theta,X):
	X=np.array(X)
	gx = 0
	for i in range(theta.size):
		gx=theta[i]*X[i]
	logit=1/(1+exp(-gx))	
	return logit

def sumhx(X,y,j,theta):
	X=np.array(X)
	y=np.array(y)
	m=X.shape[1]
	gx=0.0
	for i in range(m):
		gx=gx+(logit(theta,X[i,:])-y[i])*X[i,j]
	return gx
# grediant decent to find best theta

def plotlines(X,y,theta):
	X=np.array(X)
	y=np.array(y)
	plt.scatter(X[:,0], X[:,1], c=np.array(y), cmap=plt.cm.Paired)
	xx = np.linspace(0, 10,100)
	yy = -theta[1]/theta[2]*xx-theta[0]/theta[2]
	plt.plot(xx,yy,'k-')

for i in range(100):
	theta=gradient_decent(X,y,theta)

X=np.array(X)
plt.scatter(X[:,0], X[:,1], c=np.array(y), cmap=plt.cm.Paired)
xx = np.linspace(0, 10,100)
yy = -model.coef_[:,0]/model.coef_[:,1]*xx-model.intercept_/model.coef_[:,1]
plt.plot(xx,yy,'k-')
