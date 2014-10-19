import numpy
import scipy
import os
import sys
import DTA;
import tensor;
import ttensor;
import matplotlib.pyplot as plt
import matplotlib as mpl


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
def write(a,b):

	core = a.core
	core = core.tondarray()

	U0 = a.u[0]
	U1 = a.u[1]
	U2 = a.u[2]


	d1,d2,d3 = core.shape
	with open('core','w') as f:
		for i in range(d1):
			for j in range(d2):
				for l in range(d3):
					f.write(str(i) + ',' + str(j) + ',' + str(l) + ',' + str(core[i][j][l]) + '\n')


	d1,d2 = U0.shape
	print U0.shape
	with open('U0','w') as f:
		for i in range(d1):
			for j in range(d2):
				f.write(str(i) + ',' + str(j) + ',' + str(U0[i][j]) + '\n')


	d1,d2 = U1.shape
	print U1.shape
	with open('U1','w') as f:
		for i in range(d1):
			for j in range(d2):
				f.write(str(i) + ',' + str(j) + ',' + str(U1[i][j]) + '\n')


	d1,d2 = U2.shape
	print U2.shape
	with open('U2','w') as f:
		for i in range(d1):
			for j in range(d2):
				f.write(str(i) + ',' + str(j) + ',' + str(U2[i][j]) + '\n')




	b0 = b[0]
	d1,d2 = b0.shape
	print b0.shape
	with open('b0','w') as f:
		for i in range(d1):
			for j in range(d2):
				f.write(str(i) + ',' + str(j) + ',' + str(b0[i][j]) + '\n')


	b1 = b[1]
	d1,d2 = b1.shape
	print b1.shape
	with open('b1','w') as f:
		for i in range(d1):
			for j in range(d2):
				f.write(str(i) + ',' + str(j) + ',' + str(b1[i][j]) + '\n')


	b2 = b[2]
	d1,d2 = b2.shape
	print b2.shape
	with open('b2','w') as f:
		for i in range(d1):
			for j in range(d2):
				f.write(str(i) + ',' + str(j) + ',' + str(b2[i][j]) + '\n')


#-----------------------------------------------------------------------------------------------
if __name__ == '__main__':


	#Arguments
	dim1 = int(sys.argv[1])
	dim2 = int(sys.argv[2])
	dim3 = int(sys.argv[3])


	#Read and Save Data
	X = readData()


	#Tensor Analysis
	X = tensor.tensor(X)

	#DTA
	[a,b] = DTA.DTA(X,[dim1,dim2,dim3]);

	
	#Write out
	write(a,b)