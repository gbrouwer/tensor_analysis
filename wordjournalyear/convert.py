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
def readTopWords():

	topwords = []
	with open('data/topwords','r') as f:
		for line in f:
			elements = line.rstrip().split('\t')
			topwords.append(elements[0])

	#Return
	return topwords


#-----------------------------------------------------------------------------------------------
def readTopJournals():

	topjournals = []
	with open('data/topjournals','r') as f:
		for line in f:
			elements = line.rstrip().split('\t')
			topjournals.append(elements[0])

	#Return
	return topjournals


#-----------------------------------------------------------------------------------------------
def readData(topwords,topjournals):


	#Empty Matrix
	X = numpy.zeros((1000,100,35))


	#Loop through Data
	with open('data/wordjournalyear','r') as f:
		for line in f:
		#for i in range(10):
			#line = f.readline()
			elements = line.rstrip().split('\t')
			nOcc = int(elements[1])
			strip = elements[0][1:-1].split(',')
			year = int(strip[2])
			if (year >= 1980):
				j = topjournals.index(strip[1])
				w = topwords.index(strip[0])
				y = year - 1980
				X[w][j][y] = 1

	#Return
	return X


#-----------------------------------------------------------------------------------------------
if __name__ == '__main__':


	#Read Top Journals
	topjournals = readTopJournals()


	#Read Top Words
	topwords = readTopWords()


	#Read and Save Data
	#X = readData(topwords,topjournals)
	#output = open('data.pkl', 'wb')
	#pickle.dump(X, output)
	#output.close()


	#Read X
	myfile = open('data.pkl', 'rb')
	X = pickle.load(myfile)
	myfile.close()


	#Tensor Analysis
	X = tensor.tensor(X)

	[a,b] = DTA.DTA(X, [3,3,3]);
	core = a.core
	U0 = a.u[0]
	U1 = a.u[1]
	U2 = a.u[2]

	print core

	"""
	print U0.shape
	print U1.shape
	print U2.shape
#	print a
	print b[0].shape
	print b[1].shape
	print b[2].shape
	#a = a.totensor();
	#print a.shape
	plt.scatter(U0[:,1],U0[:,2])
#	plt.imshow(b[2],interpolation='nearest')

	for i in range(1000):
		plt.annotate(topwords[i],xy=(U0[i,1],U0[i,2]),size=6)



#ax.annotate('local max', xy=(2, 1), xytext=(3, 1.5),
          #  arrowprops=dict(facecolor='black', shrink=0.05),
           # )
	plt.show()

	"""