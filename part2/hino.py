import os, time, math
import plotly
import plotly.plotly as py
import plotly.graph_objs as go
from point import Point
from os.path import join, basename, exists, isdir

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

def pointOnBorder(x, y, strlist):
    xl, yl = get_polygon_XYlists(strlist)
    xl.pop()
    yl.pop()
    poly = zip(xl, yl)
    n = len(poly)
    for i in range(n):
        p1x, p1y = poly[i]
        p2x, p2y = poly[(i + 1) % n]
        v1x = p2x - p1x
        v1y = p2y - p1y 
        v2x = x - p1x
        v2y = y - p1y #vector from p1 to the point in question
        if(v1x * v2y - v1y * v2x == 0): #if vectors are parallel 
            if(v1x * v1x + v1y * v1y >= v2x * v2x + v2y * v2y): #if v2 is shorter than v1
                return True
    return False

def point_in_poly(x,y,strlist):
    xl, yl = get_polygon_XYlists(strlist)
    xl.pop()
    yl.pop()
    poly = zip(xl, yl)
    
    n = len(poly)
    inside = False
    p1x ,p1y = poly[0]
    for i in range(n+1):
        p2x,p2y = poly[i % n]
        if y > min(p1y,p2y):
            if y <= max(p1y,p2y):
                if x <= max(p1x,p2x):
                    if p1y != p2y:
                        xints = (y-p1y)*(p2x-p1x)/(p2y-p1y)+p1x
                    if p1x == p2x or x <= xints:
                        inside = not inside
        p1x,p1y = p2x,p2y
    return inside

def findginv(vert,guards):
    n = len(vert)
    m = len(guards)
    guardposinlist = []
    guardsposinvert = []
    for j in range(0,m-1):
        for i in range(0,n-1):
            if vert[i] == guards[j]:
                print 'True'
                guardposinlist.append(j)
                guardsposinvert.append(i)
    return guardposinlist,guardsposinvert

def twoptgradient(x1,x2,y1,y2):
    m = (y2-y1)/(x1-x2)
    return m


def liesinpoly(x1,x2,y1,y2,vert):
    #gradient = twoptgradient(x1,x2,y1,y2)
    midx, midy = midpoint(x1,x2,y1,y2)
    if (point_in_poly(midx,midy,vert) == True or pointOnBorder(midx,midy,vert) == True):
        midx1, midy1 = midpoint(x1,midx,y1,midy)
        midx2, midy2 = midpoint(midx,x2,midy,y2)
        midx3, midy3 = midpoint(midx1,midx,midy1,midy)
        midx4, midy4 = midpoint(midx2,midx,midy2,midy)

        if ((point_in_poly(midx1,midy1,vert) == True or pointOnBorder(midx1,midy1,vert) == True) and
        (point_in_poly(midx2,midy2,vert) == True or pointOnBorder(midx2,midy2,vert) == True) and 
        (point_in_poly(midx3,midy3,vert) == True or pointOnBorder(midx3,midy3,vert) == True) and 
        (point_in_poly(midx4,midy4,vert) == True or pointOnBorder(midx4,midy4,vert) == True)):
            return True
        else:
            return False
    return False


def midpoint(x1,x2,y1,y2):
    x = (x1+x2)/2
    y = (y1+y2)/2
    return x, y

def intersection(v1,v2,w1,w2):
    #v1,v2 : points of first vector
    #w1,w2 : points of second vector
    
    intersectX = ((v1.x * v2.y - v1.y * v2.x)*(w1.x - w2.x) - (v1.x - v2.x)*(w1.x * w2.y - w1.y * w2.x)) / ((v1.x - v2.x)*(w1.y - w2.y) - (v1.y - v2.y)*(w1.x - w2.x))
    intersectY = ((v1.x * v2.y - v1.y * v2.x)*(w1.y - w2.y) - (v1.y - v2.y)*(w1.x * w2.y - w1.y * w2.x)) / ((v1.x - v2.x)*(w1.y - w2.y) - (v1.y - v2.y)*(w1.x - w2.x))

    return Point(0,intersectX,intersectY)

def cangofuther()
    

def visibiltyofguards(vert,guards):
    AllvisX =[]
    AllvisY =[]
    guardpos, posinvert = findginv(vert,guards)
    xv, yv = get_polygon_XYlists(vert)
    xv.pop()
    yv.pop()
    xg, yg = get_guards_XYlists(guards)
    guardvisX = []
    guardvixY = []
    for j in range(0,len(guards)):
        for i in range(0,len(xv)):
            a = liesinpoly(xg[j],xv[i],yg[j],yv[i],vert)
            if a == True:
                print 'Line betwwen G(%.1f, %.1f) & P(%.1f, %.1f) lies in the poly' % (xg[j],yg[j],xv[i],yv[i])

#4: (1, 2), (1, -3), (4, -3), (4, -1), (3, -1), (3, -2), (2, -2), (2, 1), (7, 1), (7, 3), (6, 3), (6, 2); (7, 1), (1, 2), (4, -1)



#guardsPolygonVertices =  readguardsfile()
#a =  guardsPolygonVertices[27]
#plotguard(a)

checkPolygonVertices, checkGuardCoordinates = readcheckfile()
num = 4
a = checkPolygonVertices[num]
b = checkGuardCoordinates[num]
c = findginv(a,b)
print 'InPoly'
d = pointOnBorder(2.333,1,a)
print d
visibiltyofguards(a,b)
#plotcheck(a,b)
#visible(a,b)

#print get_polygon_XYlists(b)
#print get_guards_XYlists(c)