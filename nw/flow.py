#Standard
import numpy
import os
import sys
import scipy.spatial
import priorityqueue
import priodict
import visualizer
import matplotlib.pyplot as plt
import matplotlib as mpl


#Globals
G = {}
V = []
frame = 0
marked = []
edgeTo = {}
distTo = {}


#------------------------------------------------------
def Dijkstra(G,start,end=None):


	#Init	
	D = {}	#Dctionary of final distances
	P = {}	#Dictionary of predecessors
	Q = priodict.priorityDictionary()
	Q[start] = 0



	#While there are elements in the priority queue	
	for v in Q:
		D[v] = Q[v]
		if v == end: 
			break
		for w in G[v]:
			vwLength = D[v] + G[v][w]
			if w in D:
				if vwLength < D[w]:
					raise ValueError
 			elif w not in Q or vwLength < Q[w]:
				Q[w] = vwLength
				P[w] = v
	
	return (D,Q,P)


#------------------------------------------------------
def runDijkstra(G,start,end):


	#Run Dijkstra
	D,Q,P = Dijkstra(G,start,end)

	#Create Path	
	path = []
	totDistance = []
	while 1:
		path.append(end)
		if end == start:
			break
		end = P[end]
	path.reverse()

	#Return
	return path


#------------------------------------------------------------------------------------
def DFS(G,v):

	#DFS recursive loop
	marked.append(v)
	if (G.has_key(v)):
		for w in G[v]:
			if w not in marked:
				edgeTo[w] = v
				DFS(G,w)


#------------------------------------------------------------------------------------
def createFlowPatterns(G):

	
	#Find all startnodes
	startnodes = []
	for g in G:
		if (len(G[g]) == 1):
			startnodes.append(g)


	#Calculate KD Tree	
	kdtree = scipy.spatial.KDTree(V,leafsize=10)


	#Create Paths
	T = numpy.zeros((V.shape[0],V.shape[0],20))
	for i in range(10000):
		randomstart = numpy.random.randint(0,V.shape[0])
		#randomstart = startnodes[randomstart]

		#Pick random point and find closest vertex
		R = numpy.random.normal(0,0.5,(1,2))
		distance,neighbor = kdtree.query(R,1)
		
		#If Not Samme start and finish
		if (randomstart != neighbor[0]):
			P = runDijkstra(G,randomstart,neighbor[0])
			print P
			for j in range(len(P)-1):
				if (j < 20):
					st = P[j]
					et = P[j+1]
					T[st,et,j] = T[st,et,j] + 1


	plt.imshow(T[:,:,0],interpolation='nearest')
	plt.show()






#------------------------------------------------------------------------------------
def loadNetwork():

	V = []
	G = {}
	with open('network','r') as f:
		nNodes = int(f.readline().rstrip())
		for i in range(nNodes):
			values = f.readline().rstrip().split(',')
			V.append((float(values[0]),float(values[1])))
		for line in f:
			values = line.rstrip().split(',')
			edge = {int(values[1]):float(values[2])}
			i = int(values[0])
			if (G.has_key(int(i))):
				G[i].update(edge)
			else:
				G[i] = edge

	#Return
	V = numpy.array(V)
	return V,G


#------------------------------------------------------------------------------------
if __name__ == '__main__':


	#Load Network
	V,G = loadNetwork()


	#Create Flow Patterns
	createFlowPatterns(G)
	

	#Visualize Graph
	#C = numpy.random.random((25,3))
	#S = numpy.ones((25,1))
	#visualizer.visualizeGraph(V,G,C,S)
