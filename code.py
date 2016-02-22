import os, time, math
import plotly
import plotly.plotly as py
import plotly.graph_objs as go
from os.path import join, basename, exists, isdir
#Imports for Triangulate, (you will need to download numpy, scipy, and matplotlib)
"""
import numpy as np
import scipy as sp
import matplotlib as mpl
import matplotlib.pyplot as plt
from scipy.spatial import Delaunay
"""

INPUT_FILE_DIR = "input/"
OUTPUT_FILE_DIR = "output/"


def readguardsfile():
	inputFileName = "guards"
	infilename = os.path.join(INPUT_FILE_DIR, inputFileName + '.pol')
	outfilename = os.path.join(INPUT_FILE_DIR, inputFileName + '.sol')
	with open(infilename, 'r') as f:
		polygons = []
		for i in range(0,30):
			line = f.readline()
			line = line.rstrip()
			while not line.startswith(':'):
				line = line.lstrip("0123456789");
			line = line.lstrip(': ')
			polygons.append(line)
		polygonVertices = []
		for polygon in polygons:
			s = polygon
			vertices = []
			tempStr = ''
			inTuple = False
			j = 0
			while j < len(s):
				if s[j] == '(':
					inTuple = True
					tempStr += s[j]
				elif s[j] == ')':
					tempStr += s[j]
					vertices.append(tempStr)
					inTuple = False
					tempStr = ''
				elif inTuple:
					tempStr += s[j]
				j += 1
			polygonVertices.append(vertices)

		return polygonVertices

def readcheckfile():
	inputFileName = "check"
	infilename = os.path.join(INPUT_FILE_DIR, inputFileName + '.pol')
	outfilename = os.path.join(INPUT_FILE_DIR, inputFileName + '.sol')
	with open(infilename, 'r') as f:
		polygons = []
		for i in range(0,20):
			line = f.readline()
			line = line.rstrip()
			while not line.startswith(':'):
				line = line.lstrip("0123456789");
			line = line.lstrip(': ')
			polygons.append(line)
		polygonVertices = []
		guardCoordinates = []
		for polygon in polygons:
			s = polygon
			vertices = []
			guards = []
			tempStr = ''
			inTuple = False
			j = 0
			while j < len(s): #polygon vertices
				if s[j] == '(':
					inTuple = True
					tempStr += s[j]
				elif s[j] == ')':
					tempStr += s[j]
					vertices.append(tempStr)
					inTuple = False
					tempStr = ''
				elif inTuple:
					tempStr += s[j]
				elif s[j] == ';':
					break
				j += 1
			inTuple = False
			while j < len(s): #guard coordinates
				if s[j] == '(':
					inTuple = True
					tempStr += s[j]
				elif s[j] == ')':
					tempStr += s[j]
					guards.append(tempStr)
					inTuple = False
					tempStr = ''
				elif inTuple:
					tempStr += s[j]
				j += 1
			polygonVertices.append(vertices)
			guardCoordinates.append(guards)

		return polygonVertices, guardCoordinates

def get_polygon_XYlists(singlePolygon): #takes in one list of vertices for a selected polygon
	listLength = len(singlePolygon)
	Xlist = []
	Ylist = []
	for vertice in singlePolygon:
		coordinates = vertice.strip('()')
		coordinates = coordinates.split(',')
		x = coordinates[0]
		x = float(x)
		y = coordinates[1]
		y = float(y)
		Xlist.append(x)
		Ylist.append(y)
	firstVertice = singlePolygon[0]
	coordinates = firstVertice.strip('()')
	coordinates = coordinates.split(',')
	x = coordinates[0]
	x = float(x)
	y = coordinates[1]
	y = float(y)
	Xlist.append(x)
	Ylist.append(y)
	return Xlist, Ylist

def get_guards_XYlists(singlePolygon): #takes in one list of vertices for a selected polygon
	listLength = len(singlePolygon)
	Xlist = []
	Ylist = []
	for vertice in singlePolygon:
		coordinates = vertice.strip('()')
		coordinates = coordinates.split(',')
		x = coordinates[0]
		x = float(x)
		y = coordinates[1]
		y = float(y)
		Xlist.append(x)
		Ylist.append(y)
	return Xlist, Ylist

def triangulate(singlePolygon):
	points = np.array(singlePolygon)
	tri = Delaunay(points)
	return tri

def plotguard(singlePolygon):
	from plotly.graph_objs import Scatter, Layout
	polXlist, polYlist = get_polygon_XYlists(singlePolygon)
	plotly.offline.plot({
	"data": [
    Scatter(x=polXlist, y=polYlist, fill='tozeroy'),
    ]
	})


def plotcheck(singlePolygon,guard):
	from plotly.graph_objs import Scatter, Layout
	polXlist, polYlist = get_polygon_XYlists(singlePolygon)
	guardXlist, guardYlist = get_guards_XYlists(guard)
	plotly.offline.plot({
	"data": [
    Scatter(x=polXlist, y=polYlist, fill='tozeroy'),
    Scatter(x=guardXlist, y=guardYlist, mode = 'markers')
	]
	})


guardsPolygonVertices =  readguardsfile()
a =  guardsPolygonVertices[0]
plotguard(a)

#checkPolygonVertices, checkGuardCoordinates = readcheckfile()
#a = checkPolygonVertices[2]
#b = checkGuardCoordinates[2]
#plotcheck(a,b)
