#Standard
import numpy
import os
import sys
import scipy.spatial
import priorityqueue
import priodict


#Globals
G = {}
V = []
marked = []
edgeTo = {}
distTo = {}



#------------------------------------------------------------------------------------
def createNodes(nNodes):

	#Create Vertices
	V = numpy.random.normal(0,0.5,(nNodes,2))
	V[0,0] = 0
	V[0,1] = 0

	#Return
	return V


#------------------------------------------------------------------------------------
def createEdges(V,minDistance):


	#KD Distance Tree
	kdtree = scipy.spatial.KDTree(V,leafsize=10)


	#Find Edges
	nNodes = V.shape[0]
	for i in range(nNodes):

		#Get neighbors
		node = V[i,:]
		distances,neighbors = kdtree.query(node,nNodes)
		indices = neighbors[numpy.where(distances < minDistance)[0]][1:]
		distances = distances[1:]

		#Add Edges
		for index,j in enumerate(indices):
			edge1 = {j:distances[index]}
			edge2 = {i:distances[index]}
			if (G.has_key(i)):
				G[i].update(edge1)
			else:
				G[i] = edge1
			if (G.has_key(j)):
				G[j].update(edge2)
			else:
				G[j] = edge2


	#Return
	return G


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
def computeMST(G):


	#New Graph
	MST = {}
	pq = priorityqueue.PriorityQueue('min')


	#Create Edge List From Graph
	for g in G:
		for v in G[g]:
			mytuple = G[g][v],(g,v)
			pq.push(mytuple)


	while (not pq.isempty()):
		d,edge = pq.pop()
		v,w = edge
		marked[:] = []
		DFS(MST,v)
		if w not in marked:
			edge1 = {w:d}
			edge2 = {v:d}
			if (MST.has_key(v)):
				MST[v].update(edge1)
			else:
				MST[v] = edge1
		
			if (MST.has_key(w)):
				MST[w].update(edge2)
			else:
				MST[w] = edge2

	#Return 
	return MST



#------------------------------------------------------------------------------------
def saveNetwork(G,V):

	#Save Network
	nNodes = V.shape[0]
	with open('network','w') as f:

		#Write Vertices
		f.write(str(nNodes) + '\n')
		for i in range(nNodes):
			f.write(str(V[i,0]) + ',' + str(V[i,1]) + '\n')

		#Write Edges
		for g in G:
			for v in G[g]:
				f.write(str(g) + ',' + str(v) + ',' + str(G[g][v]) + '\n')


#------------------------------------------------------------------------------------
if __name__ == '__main__':


	#Init
	nNodes = 25
	minDistance = 1.0


	#Create network
	V = createNodes(nNodes)


	#Create Preferential Edges
	G = createEdges(V,minDistance)


	#Minimum Spanning Tree
	G = computeMST(G)


	#Save Network
	saveNetwork(G,V)

