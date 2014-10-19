#Standard
import numpy
import os
import sys
import scipy.spatial
import priorityqueue
import priodict
import visualizer


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
def createTransitionMatrix(G):


	#For each node, compute the shortest route from its neighbors to center node
	C = numpy.zeros((V.shape[0],3))
	startnodes = []
	T = numpy.zeros((V.shape[0],V.shape[0]))
	for g in G:


		#Compute distances from neighbor node to center
		distances = []
		for w in G[g]:
			P = runDijkstra(G,w,0)
			totDis = 0;
			for m in range(len(P)-1):
				totDis = totDis + G[P[m]][P[m+1]]
			distances.append((w,totDis))


		#Normalize distances and add self loop
		totDis = 0
		newdistances = []
		for mytuple in distances:
			w,dis = mytuple
			totDis = totDis + dis
		if (len(distances) > 1):
			divider = ((len(distances) - 2) + len(distances)) * 0.80
			for mytuple in distances:
				w,dis = mytuple
				dis = ((1 - (dis / totDis)) / divider)
				mytuple = w,dis
				newdistances.append(mytuple)
			newdistances.append((g,0.3750))
		if (len(distances) == 1):
			mytuple = distances[0]
			w,dis = mytuple
			startnodes.append(g)
			newdistances.append((w,0.62500))
			newdistances.append((g,0.37500))


		#Add to Transition Matrix
		for mytuple in newdistances:
			w,dis = mytuple
			T[w,g] = dis


		#Color Coding
		distances = numpy.asarray(distances)
		mindis = numpy.min(distances)
		C[g,0] = mindis
		C[g,1] = mindis
		C[g,2] = mindis

	
	C = C / numpy.max(C)
	C[:,1] = 1 - C[:,1]


	#Return
	return T,C,startnodes


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


	#Create Transition Matrix
	T,C,startnodes = createTransitionMatrix(G)
	
	print numpy.sum(T,axis=0)
	#Init Random Walk
	S = numpy.zeros((V.shape[0],100))
	v = numpy.zeros((V.shape[0],1))
	for startnode in startnodes:
		v[startnode,0] = 2.0
	S[:,0] = v[:,0]

	#Start Random Walk
	for i in range(99):
		v = numpy.dot(T,v)
		S[:,i+1] = v[:,0]


	#Visualize Graph
	visualizer.visualizeGraph(V,G,C,S)
