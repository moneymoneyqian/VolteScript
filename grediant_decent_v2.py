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
	error=y-logit(theta,X)
	tmp=np.dot(X.transpose(),error)
	theta=theta - step*1/m*tmp
	return theta
                                             
def logit(theta,X):
	X=np.array(X)
	gx = 0
	gx=np.dot(X,theta)
	logit=1/(1+exp(-gx))	
	return logit

def sumhx(X,y,j,theta):
	X=np.array(X)
	y=np.array(y)
	m=X.shape[0]
	gx=0.0
	for i in range(m):
		gx=gx+(logit(theta,X[i,:])-y[i])*X[i,j]
	return gx
# grediant decent to find best xx-theta

def plotlines(X,y,theta):
	X=np.array(X)
	y=np.array(y)
	plt.scatter(X[:,0], X[:,1], c=np.array(y), cmap=plt.cm.Paired)
	xx = np.linspace(-10, 10,100)
	yy = -theta[1]/theta[2]*xx-theta[0]/theta[2]
	plt.plot(xx,yy,'k-')

theta=np.array([0.0,0.0,0.0])
for i in range(500):
	theta=gradient_decent(X,y,theta,step=0.0001)

theta=np.ones((3,1))
X=np.array(X)
plt.scatter(X[:,0], X[:,1], c=np.array(y), cmap=plt.cm.Paired)
xx = np.linspace(0, 10,100)
yy = -model.coef_[:,0]/model.coef_[:,1]*xx-model.intercept_/model.coef_[:,1]
plt.plot(xx,yy,'k-')



# test'
Xtmp=np.array(pd.concat([ones,X],axis=1))
y=np.array(y)
theta=np.ones((3,1))
for i in range(20):
	error=logit(theta,Xtmp)-y
	tmp=np.dot(Xtmp.transpose(),error)
	theta=theta + step*1/m*tmp
	print theta[0]/theta[2]
	plotlines(X,y,theta)