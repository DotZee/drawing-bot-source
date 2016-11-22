import Edge

from math import asin, pi, sin , cos, sqrt
from PIL import Image
import cv2
import time

#global image
img = None

path = [[]]
pthpts = []
pix = []

lm = 4

swtchr = {0:(-1,-1), 1:(0,-1), 2:(1,-1), 3:(1,0),
            4:(1,1), 5:(0,1), 6:(-1,1), 7:(-1,0)}

invswt = dict(zip(swtchr.values(), swtchr.keys()))

def abc(t):

    x = t[0]
    y = t[1]
    
    if x==0:
        x += 0.0001
    if y == 0:
        y += 0.0001
    
    theta = 0           #Angle moved by arm
    psi = 0             #Angle moved by rotor
    r = sqrt(x**2 + y**2)
    
    theta = 2*asin(r/(2*R))
    d = sqrt((x - R*sin(theta))**2 + (y - R*(1 - cos(theta)))**2)
    psi = 2*asin(d/(2*r))

    #Changing to degrees
    theta = 180*theta/pi
    psi = 180*psi/pi

    psi = signum(x**2 + (y - R)**2 - R**2) * signum(x) * psi

    
    if abs(theta) > 60 or abs(psi) > 90:
        return None
    
    return (theta, psi)



def signum(x):
    if x < 0:
        return -1
    elif x == 0:
        return 0
    else:
        return 1

def tocart(x,y):
    global size
    h = x - (size[0]//2)
    k = (size[1]//2) - y
    return (h,k)

    

lastk = 0
    
def nxtpt(pt):
    global path
    global pthpts
    global pix
    global lastk

    n = False
    
    '''
    if len(path[-1] > 2):
        prev = path[-1][-2]

        print path
        print prev
        
        inv = (pt[0] - prev[0], pt[1] - prev[1])
        inv = invswt[inv]
    else:
        inv = (0,0)
    '''

    '''
    n = False
    
    for k in range(lastk, 8 + lastk):
        k = k%8
        nxt = (pt[0] + swtchr[k][0], pt[1] + swtchr[k][1])

        if 0 <= nxt[0] < size[0] and 0 <= nxt[1] < size[1] and nxt in pix:
            if not bool(n):
                lastk = k
                n = nxt
            else:
                if nxt not in pthpts:
                    pthpts.append(nxt)
    
    
    '''
    for k in range(1,8,2):
        
        nxt = (pt[0] + swtchr[k][0], pt[1] + swtchr[k][1])

        if 0 <= nxt[0] < size[0] and 0 <= nxt[1] < size[1] and nxt in pix:
            if not bool(n):
                n = nxt
            else:
                if nxt not in pthpts:
                    pthpts.append(nxt)

    for k in range(0,8,2):
        
        nxt = (pt[0] + swtchr[k][0], pt[1] + swtchr[k][1])

        if 0 <= nxt[0] < size[0] and 0 <= nxt[1] < size[1] and nxt in pix:
            if not bool(n):
                n = nxt
            else:
                if nxt not in pthpts:
                    pthpts.append(nxt)
    
    
    return n

def getnewpt():
    newpt = None
    if len(pthpts)>0:
        newpt = pthpts[-1]
    while newpt not in pix:
        if len(pthpts) > 0:
            newpt = pthpts[-1]
            del pthpts[-1]
        else:
            newpt = pix[int(len(pix)/2)]

    return newpt

def avg(t):

    if type(t) == type(1):
        return t
    
    a = 0
    for k in t:
        a += k
    return float(a)/len(t)

def impath(im, showpath = True):

    if im.mode != '1':
        im = im.convert('1')
        
    
    if type(im) is str:
        im = Image.open(im)
    
    global R
    pixels = im.load()
    global path     #paths list
    path = [[]]
    global pthpts
    pthpts = []#other potential starting points
    global pix
    pix = []        #list of all points to be in path
    global size
    size = im.size

    global img
    img = im

    print 'mode' , im.mode
    
    R = pow(size[0]**2 + size[1]**2, 0.5)*0.5

    #print im
    
    for x in range(im.size[0]):
        for y in range(im.size[1]):
            if avg(pixels[x,y]) ==  0:
                #print 'colour of' , x,y, '=', pixels[x,y]
                pix.append((x,y))

    
    #print len(pix)
    pt = pix[0]
    newpt = pt
    i =0
    while len(pix) > 1:
        
        i+=1
        #print 'iteration:', i
        pt = newpt
        #print pt
        pix.remove(pt)
        
        path[-1].append(pt)
        
        newpt = nxtpt(pt)
        
        #print 'newpt', newpt
        if newpt == False:
            
            path.append([])
            #print 'getting new point'
            
            #print 'path points', pthpts
            newpt = getnewpt()

    while [] in path:
        path.remove([])

    if showpath:
        show(im, path)

    return path

def show(im, p):
    im.save('deletethisfileifyouwish.png')

    imnew = cv2.imread('deletethisfileifyouwish.png')
    for k in path:
        for c in k:
            cv2.waitKey(1)
            imnew[c[1],c[0]] = [255,100,255]
            cv2.imshow('A', cv2.resize(imnew, None, fx = 5, fy = 5))
        #print k

    print 'PRESS ANY KEY TO CLOSE SIMULATION'
    cv2.waitKey(0)
    cv2.destroyAllWindows()

#main
'''
a = Edge.edge(Image.open('A.png'))
a.save('edge.png')
p = impath(a)
print 'path length : ', len(path)

imnew = cv2.imread('edge.png')
for k in path:
    for c in k:
        cv2.waitKey(1)
        imnew[c[1],c[0]] = [255,100,255]
        cv2.imshow('A', cv2.resize(imnew, None, fx = 5, fy = 5))
    print k
cv2.waitKey(0)
cv2.destroyAllWindows()

'''
