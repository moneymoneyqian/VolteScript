import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
X = pd.read_csv('E:/sample/5.1.logistic_x.txt',sep=',',header=None,names=('v1','v2'))
Xtmp = pd.read_csv('E:/sample/5.1.logistic_x.txt',sep=',',header=None,names=('v1','v2'))

ones=pd.Series(np.ones(X.shape[0]))
X=np.array(pd.concat([ones,X],axis=1))
y = pd.read_csv('E:/sample/5.1.logistic_y.txt',sep=',',header=None,names=('y'))
y = np.array(y)

def loadDataSet():
	dataMat = []; labelMat = []
	fr = open('E:/sample/5.1.logistic_x.txt')
	for line in fr.readlines():
		lineArr = line.strip().split(",")
		dataMat.append([1.0, float(lineArr[0]), float(lineArr[1])])
	return dataMat


def sigmoid(inX):
	return 1.0/(1+exp(-inX))


def gradAscent(dataMatIn, classLabels,tehta):
	dataMatrix = mat(dataMatIn)
	labelMat = mat(classLabels).transpose()
	m,n = shape(dataMatrix)
	alpha = 0.001
	weights = theta
	h = sigmoid(np.dot(dataMatrix,weights))
	error = (y - h)
	weights = weights + alpha * dataMatrix.transpose()* error
	# print "h="
	# print h
	# print "error"
	# print error
	# print "dataMatrix.transpose()* error="
	# print dataMatrix.transpose()* error
	return weights

theta=np.ones((3,1))
for i in range(20):
	theta=gradAscent(X,y,theta)
	plotlines(Xtmp,y,theta)

def plotlines(X,y,theta):
	X=np.array(X)
	y=np.array(y)
	plt.scatter(X[:,0], X[:,1], c=np.array(y), cmap=plt.cm.Paired)
	xx = np.linspace(-0, 10,100)
	yy = -theta[1]/theta[2]*xx-theta[0]/theta[2]
	plt.plot(xx,yy.transpose(),'k-')