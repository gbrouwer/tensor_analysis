#Standard
import numpy
import os
import sys
import scipy.spatial
import priorityqueue
import priodict


#OpenGL
import OpenGL.GLUT as glut
from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *


#Vispy
from vispy import gloo
from vispy import app
from vispy.gloo import gl


#Globals
G = {}
V = []
frame = 0
marked = []
edgeTo = {}
distTo = {}



#------------------------------------------------------------------------------------
def on_display():

	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
	glClearDepth(10)
	glFlush()
	draw()
	glutSwapBuffers()
	glutPostRedisplay()


#------------------------------------------------------------------------------------
def on_keyboard(key, x, y):

	if key == '\033':
		sys.exit()


#------------------------------------------------------------------------------------
def on_reshape(w, h):

	#Reshape
	glMatrixMode(GL_PROJECTION);
	glLoadIdentity();
	gluPerspective(20.0, float(w)/float(h), 0.1, 100.0);
	glMatrixMode( GL_MODELVIEW );
	glViewport( 0, 0, w, h );	
	

#------------------------------------------------------------------------------------
def on_idle():

	#Advances frame
	global frame
	t = glut.glutGet(glut.GLUT_ELAPSED_TIME)
	frame = frame + 30
	if (frame > 1439):
		frame = frame - 1439 
	#print t


#------------------------------------------------------------------------------------
def draw():


	#Anti-alaising
	glEnable(GL_POINT_SMOOTH);
	glEnable(GL_LINE_SMOOTH);
	glHint(GL_POINT_SMOOTH_HINT, GL_NICEST);
	glHint(GL_LINE_SMOOTH_HINT, GL_NICEST);


	#Clear and Push
	glClearColor(0,0,0,1)
	glPushMatrix()


	#Draw nodes
	glPointSize(10)
	glBegin(GL_POINTS)
	nNodes = V.shape[0]
	for i in range(nNodes):
		node = V[i,:]
		glVertex3f(node[0],0,node[1])
	glEnd()


	#Draw Edges
	glBegin(GL_LINES)
	for g in G:
		for v in G[g]:
			node1 = V[g,:]
			node2 = V[v,:]
			glVertex3f(node1[0],0,node1[1])
			glVertex3f(node2[0],0,node2[1])
	glEnd()


	#Pop
	glPopMatrix()


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
	for g in G:
		print '----'
		distances = []
		for w in G[g]:
			P = runDijkstra(G,w,0)
			totDis = 0;
			for m in range(len(P)-1):
				totDis = totDis + G[P[m]][P[m+1]]
			distances.append((w,totDis))
		print distances

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
	#for val in range(10):
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
def visualizeGraph():


	#Init Glut
	glut.glutInit(sys.argv)
	glut.glutInitDisplayMode(glut.GLUT_DOUBLE | glut.GLUT_RGB | glut.GLUT_DEPTH)
	glut.glutInitWindowSize(1024,1024)
	glut.glutCreateWindow(" Visualize (GLUT)")
	glut.glutDisplayFunc(on_display)
	glut.glutKeyboardFunc(on_keyboard)
	glut.glutReshapeFunc(on_reshape);


	#Lookat	
	gluLookAt(0,12,0,  0,0,0,  0,0,1);
	

	#Idle function
	glut.glutIdleFunc(on_idle)
	#glut.glutFullScreen()
	glut.glutMainLoop()


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


	#Create Transition Matrix
	T = createTransitionMatrix(G)



	
	#Visualize Graph
	#visualizeGraph()
