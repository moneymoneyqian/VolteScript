import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

X = pd.read_csv('E:/sample/5.1.logistic_x.txt',sep=',',header=None,names=('v1','v2'))
Xtmp = pd.read_csv('E:/sample/5.1.logistic_x.txt',sep=',',header=None,names=('v1','v2'))
Xtmp = np.array(Xtmp)
y = pd.read_csv('E:/sample/5.1.logistic_y.txt',sep=',',header=None,names=('y'))


#use sklearn to fit model
from sklearn.linear_model import LogisticRegression
model = LogisticRegression(solver='newton-cg')
model.fit(X,y)

# grediant decent to find best theta
def gradient_decent(X,y,theta,step=0.001):
	X=pd.DataFrame(X)
	ones=pd.Series(np.ones(X.shape[0]))
	X=np.array(pd.concat([ones,X],axis=1))
	y=np.array(y);
	m=X.shape[0]
	error=y-logit(np.dot(X,theta))
	tmp=np.dot(X.transpose(),error)
	theta=theta + step*1/m*tmp
	# print "error"
	# print error
	# print "tmp"
	# print tmp
	return theta
                                             
def logit(inX):
	return 1.0/(1+exp(-inX))

def sumhx(X,y,j,theta):
	X=np.array(X)
	y=np.array(y)
	m=X.shape[0]
	gx=0.0
	for i in range(m):
		gx=gx+(logit(theta,X[i,:])-y[i])*X[i,j]
	return gx
# grediant decent to find best xx-theta

def plotlines(X,y,theta,linecolor="black"):
	X=np.array(X)
	y=np.array(y)
	plt.scatter(X[:,0], X[:,1], c=np.array(y), cmap=plt.cm.Paired)
	xx = np.linspace(-0.0, 10,100)
	yy = -theta[1]/theta[2]*xx-theta[0]/theta[2]
	plt.plot(xx,yy,'k-',color=linecolor)

theta=np.ones((3,1))
for i in range(200):
	theta=gradient_decent(X,y,theta,step=1)
	plotlines(Xtmp,y,theta,linecolor="red")

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