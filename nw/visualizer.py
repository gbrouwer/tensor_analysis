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
frame = 0
V = []
G = {}
C = []
S = []

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
	frame = frame + 1
	if (frame > 50):
		frame = frame - 50
	print frame


#------------------------------------------------------------------------------------
def draw():


	#Anti-alaising
	glEnable(GL_POINT_SMOOTH);
	glEnable(GL_LINE_SMOOTH);
	glHint(GL_POINT_SMOOTH_HINT, GL_NICEST);
	glHint(GL_LINE_SMOOTH_HINT, GL_NICEST);


	#Clear and Push
	glClearColor(0,0.1,0.2,1)
	glPushMatrix()


	#Draw Edges
	glColor3f(0.5,0.5,0.5)
	glBegin(GL_LINES)
	for g in G:
		for v in G[g]:
			node1 = V[g,:] * 1.25
			node2 = V[v,:] * 1.25
			glVertex3f(node1[0],0,node1[1])
			glVertex3f(node2[0],0,node2[1])
	glEnd()


	#Draw nodes
	glPointSize(10)
	nNodes = V.shape[0]
	for i in range(nNodes):
		node = V[i,:] * 1.25
		glColor3f(C[i,0],C[i,1],C[i,2])
		glBegin(GL_POLYGON)
		for j in range(0,360,10):
			x = float(j) / 180 * 3.14159275
			y = float(j) / 180 * 3.14159275
			x = numpy.sin(x) * 0.1 * S[i,frame]
			y = numpy.cos(y) * 0.1 * S[i,frame]
			glVertex3f(node[0]+x,0.001,node[1]+y)
		glEnd()




	#Pop
	glPopMatrix()



#------------------------------------------------------------------------------------
def visualizeGraph(V1,G1,C1,S1):


	#Assign
	global V
	global G
	global C
	global S
	V = V1
	G = G1
	C = C1
	S = S1

	#Take Log
	S = numpy.log(S + 1)


	#Init Glut
	glut.glutInit(sys.argv)
	glut.glutInitDisplayMode(glut.GLUT_DOUBLE | glut.GLUT_RGB | glut.GLUT_DEPTH)
	glut.glutInitWindowSize(1024,1024)
	glut.glutCreateWindow("Visualize (GLUT)")
	glut.glutDisplayFunc(on_display)
	glut.glutKeyboardFunc(on_keyboard)
	glut.glutReshapeFunc(on_reshape);


	#Lookat	
	gluLookAt(0,12,0,  0,0,0,  0,0,1);
	

	#Idle function
	glut.glutIdleFunc(on_idle)
	glut.glutFullScreen()
	glut.glutMainLoop()


