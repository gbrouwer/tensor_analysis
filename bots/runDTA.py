import numpy
import scipy
import os
import sys
import DTA;
import tensor;
import ttensor;
import matplotlib.pyplot as plt
import matplotlib as mpl
import pickle



#-----------------------------------------------------------------------------------------------
def readData():




	#Loop through Data
	with open('tensor','r') as f:
		
		#Read Dimensions
		line = f.readline().rstrip()
		elements = line.split(',')
		xdim = int(elements[0])
		ydim = int(elements[1])
		zdim = int(elements[2])

		#Empty Matrix
		X = numpy.zeros((xdim,ydim,zdim))
		
		for line in f:
			elements = line.rstrip().split(',')
			xin = int(elements[0])-1
			yin = int(elements[1])-1
			zin = int(elements[2])-1
			value = float(elements[3])
			X[xin,yin,zin] = value

	#Return
	return X


#-----------------------------------------------------------------------------------------------
if __name__ == '__main__':



	#Read and Save Data
	X = readData()


	#Tensor Analysis
	X = tensor.tensor(X)

	[a,b] = DTA.DTA(X, [2,2,2]);
	core = a.core
	U0 = a.u[0]
	U1 = a.u[1]
	U2 = a.u[2]

	print core


#	print U0.shape
#	print U1.shape
#	print U2.shape
#	print a
#	print b[0].shape
#	print b[1].shape
#	print b[2].shape
#	#a = a.totensor();
#	#print a.shape
	#print U0
	#print U1
	#plt.scatter(U2[:,0],U2[:,1])
	#plt.show()

	