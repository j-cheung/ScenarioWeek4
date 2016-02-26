import os, time, math
import plotly
import plotly.plotly as py
import plotly.graph_objs as go


from decimal import Decimal
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


def plotcheck(singlePolygon,guard,AllvisX, AllvisY):
    from plotly.graph_objs import *
    from plotly.graph_objs import Scatter, Layout
    polXlist, polYlist = get_polygon_XYlists(singlePolygon)
    guardXlist, guardYlist = get_guards_XYlists(guard)

    data = [Scatter(x=polXlist, y=polYlist, fill='tozeroy'),Scatter(x=guardXlist, y=guardYlist, mode = 'markers')]

    

    
    for j in range(len(guardvisX)):
        a = zip(polXlist,polYlist)
        for k in range(len(guardvisX[j])-1,-1,-1):
        #for k in range(0,len(guardvisX[j])):
            aa = guardvisX[j]
            bb = guardvisY[j]
            aaa =[]
            bbb =[] 
            ax,ay = pointOnBorderRe(aa[k],bb[k],singlePolygon)
            print ax,ay
            aaa.append(ax)
            bbb.append(ay)
            b = zip(aaa,bbb)
            
            #print aaa,bbb
            c = a.index(b[0])

            #print a[c] == b[0]
            d = zip(AllvisX[j],AllvisY[j])
            
            e = d[len(d)-1]
            hh = 0
            found = False
            for i in range(len(d)):
                if d[i] == b[0]:
                    hh = b[0]
                    found = True

            if found == False:
                counter = c -1
                while found == False:
                    if counter == -1:
                        counter = len(a) -1
                    for i in range(len(d)):
                        if a[counter] == d[i]:
                            hh = d[i]
                            found = True
                            break;
                    counter = counter - 1         
            g = len(AllvisX[j])-1

            print 'hhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh'
            print hh

            while (d[g] != hh):
                g = g - 1
                if (d[g] == hh or g == 0) :
                    break

            AllvisX[j].insert(g+1,aa[k])
            AllvisY[j].insert(g+1,bb[k])
            h = zip(aa,bb)
            a.insert(c,h[k])
                        


    #print AllvisX, AllvisY
    
    #for i in range(len(AllvisX)):
    for i in range(7,8):
        guardseeareaX = []
        guardseeareaY = []
        for j in range(len(AllvisX[i])):
            a = AllvisX[i]
            b = AllvisY[i]
            guardseeareaX.append(a[j])
            guardseeareaY.append(b[j])
        guardseeareaX.append(guardseeareaX[0])
        guardseeareaY.append(guardseeareaY[0])
        
        print zip(guardseeareaX, guardseeareaY)
        trace = Scatter(x=guardseeareaX, y=guardseeareaY, fill='tozeroy', fillcolor='yellow')
        data.append(trace)


    trace = Scatter(x=guardXlist, y=guardYlist, mode = 'markers', marker=Marker(color = 'red',size = '20'))
    data.append(trace)
    plotly.offline.plot(data)

def distance(x1,y1,x2,y2):
    return math.sqrt((x1 - x2)**2 + (y1 - y2)**2)

def is_between(x1,y1,x,y,x2,y2):
    return distance(x1,y1,x,y) + distance(x,y,x2,y2) == distance(x1,y1,x2,y2)

def pointOnBorder(x,y,strlist):
    xl, yl = get_polygon_XYlists(strlist)
    xl.pop()
    yl.pop()
    poly = zip(xl, yl)

    n = len(poly)
    for i in range(n):
        x1,y1 = poly[i]
        x2,y2 = poly[(i + 1) % n]
        if is_between(x1,y1,x,y,x2,y2) == True:
            return True
    return False

def pointOnBorderRe(x,y,strlist):
    xl, yl = get_polygon_XYlists(strlist)
    xl.pop()
    yl.pop()
    poly = zip(xl, yl)

    n = len(poly)
    for i in range(n):
        x1,y1 = poly[i]
        x2,y2 = poly[(i + 1) % n]
        if is_between(x1,y1,x,y,x2,y2) == True:
            return x1,y1
    

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
    if (x1 == x2 and y1 == y2):
        return 100000001
    elif x1 == x2: #Vertical
        return 0
    elif y1 == y2: #Hori
        return 1000000
    else:
        m = (y2-y1)/(x2-x1)
    return m

def liesinpoly(x1,x2,y1,y2,vert):
    #gradient = twoptgradient(x1,x2,y1,y2)
    midx, midy = midpoint(x1,x2,y1,y2)
    #print midx,midy
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


def cangofuther(xg,yg,xv,yv,vert):
    x = 0
    y = 0

    if (xg == xv and yg == yv):
        return False
    elif xg == xv: #Vertical
        
        if yg > yv:
            y = yv - 0.1
        else:
            y = yv + 0.1
        if ((point_in_poly(xg,y,vert) == False and pointOnBorder(xg,y,vert) == False)):
            return False
    elif yg == yv: #Hori
        if xg > xv:
            x = xv - 0.1
        else:
            x = xv + 0.1
        if ((point_in_poly(x,yg,vert) == False and pointOnBorder(x,yg,vert) == False)):
            return False
    else:
        m = twoptgradient(xg,xv,yg,yv)
        if ((m < 0 and yg < yv) or (m > 0 and yg > yv)):
            x = xv - 0.1 
            y = (m*(x-xg))+yg
        elif((m < 0 and yg > yv) or (m > 0 and yg < yv)):         
            x = xv + 0.1 
            y = (m*(x-xg))+yg
            #print x,y
        if ((point_in_poly(x,y,vert) == False and pointOnBorder(x,y,vert) == False)):
            return False
    return True

    
def intersection(xg,yg,xv,yv,vert):
    #v1,v2 : points of first vector
    #w1,w2 : points of second vector
    xl, yl = get_polygon_XYlists(vert)
    xl.pop()
    yl.pop()
    poly = zip(xl, yl)
    n = len(poly)
    for i in range(n):
        x1,y1 = poly[i]
        x2,y2 = poly[(i + 1) % n]
        if twoptgradient(xg,xv,yg,yv) != twoptgradient(x1,x2,y1,y2):
            intersectX = ((xg * yv - yg * xv)*(x1 - x2) - (xg - xv)*(x1 * y2 - y1 * x2)) / ((xg - xv)*(y1 - y2) - (yg - yv)*(x1 - x2))
            intersectY = ((xg * yv - yg * xv)*(y1 - y2) - (yg - yv)*(x1 * y2 - y1 * x2)) / ((xg - xv)*(y1 - y2) - (yg - yv)*(x1 - x2))
            a = pointOnBorder(intersectX,intersectY,vert)
            if ((a == True) and (distance(xg,yg,intersectX,intersectY) > distance(xg,yg,xv,yv))):
                m = twoptgradient(xg,xv,yg,yv)

                if ((m < 0 and yg < yv and yv < intersectY) or (m > 0 and yg > yv and yv > intersectY)):
                    print intersectX,intersectY
                    #intersectX = float(intersectX)
                    #intersectY = float(intersectY)
                    TempX.append(intersectX)
                    TempY.append(intersectY)
                    #return intersectX, intersectY                    
                elif((m < 0 and yg > yv and yv > intersectY) or (m > 0 and yg < yv and yv < intersectY)):    
                    print intersectX,intersectY
                    #intersectX = float(intersectX)
                    #intersectY = float(intersectY)
                    TempX.append(intersectX)
                    TempY.append(intersectY)
                    #return intersectX, intersectY
                elif (m == 0 or m == 1000000):
                    print intersectX,intersectY
                    TempX.append(intersectX)
                    TempY.append(intersectY)
    return
    

def visibiltyofguards(vert,guards):
    AllvisX =[]
    AllvisY =[]
    guardvertvisX=[]
    guardvertvisY=[]
    

    guardpos, posinvert = findginv(vert,guards)
    xv, yv = get_polygon_XYlists(vert)
    xv.pop()
    yv.pop()
    xg, yg = get_guards_XYlists(guards)
    for j in range(0,len(guards)):
        for i in range(0,len(xv)):
            a = liesinpoly(xg[j],xv[i],yg[j],yv[i],vert)
            if a == True:
                print 'Line between G(%.1f, %.1f) & P(%.1f, %.1f) lies in the poly' % (xg[j],yg[j],xv[i],yv[i])
                guardvertvisX.append(xv[i])
                guardvertvisY.append(yv[i])
                b = cangofuther(xg[j],yg[j],xv[i],yv[i],vert)
                if b == False:
                    print 'No'
                else:
                    print 'Yes'
                    intersection(xg[j],yg[j],xv[i],yv[i],vert)


        AllvisX.append(guardvertvisX)
        AllvisY.append(guardvertvisY)
        guardvertvisX=[]
        guardvertvisY=[]
        guardvisX.append(TempX)
        guardvisY.append(TempY)
        B()



    print AllvisX, AllvisY
    print guardvisX, guardvisY
    return AllvisX, AllvisY
    

def A():
    global guardvisX
    guardvisX = []

    global guardvisY
    guardvisY = []

def B():
    global TempX
    TempX = []

    global TempY
    TempY = []
def C():
    global locationX
    locationX = 0
    global locationY
    locationY = 0



#4: (1, 2), (1, -3), (4, -3), (4, -1), (3, -1), (3, -2), (2, -2), (2, 1), (7, 1), (7, 3), (6, 3), (6, 2); (7, 1), (1, 2), (4, -1)



#guardsPolygonVertices =  readguardsfile()
#a =  guardsPolygonVertices[27]
#plotguard(a)
A()
B()
C()
checkPolygonVertices, checkGuardCoordinates = readcheckfile()
num = 0
a = checkPolygonVertices[num]
b = checkGuardCoordinates[num]
c = findginv(a,b)
print a
print 'InPoly'
d = pointOnBorder(1.75,1.625,a)
print d
AllvisX, AllvisY = visibiltyofguards(a,b)
plotcheck(a,b,AllvisX, AllvisY)
#visible(a,b)

#print get_polygon_XYlists(b)
#print get_guards_XYlists(c)