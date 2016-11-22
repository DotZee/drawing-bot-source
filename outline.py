from math import sqrt, sin, cos, asin, pi
import Edge as edgeModule
import path as pathModule
from PIL import Image


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
#    if not(-1 <= r/(2*R) <= 1): 
#        return None

#Very important to make theta -ve according to sign of x
#it took me long to figure this out
#Ashish 14-06-2016 (11 days to birthday)
    theta = 2*asin(r/(2*R))*signum(x)
    d = sqrt((x - R*sin(theta))**2 + (y - R*(1 - cos(theta)))**2)
#    if not(-1 <= d/2*r <= 1):
#        return None
    psi = 2*asin(d/(2*r))

    #Changing to degrees
    theta = 180*theta/pi
    psi = 180*psi/pi


    #Inside arm circle
    #   -- x > 0
    #       --p < 0
    #   -- x < 0
    #       --p > 0
    #Outside arm circle
    #   -- x > 0
    #       --p > 0
    #   -- x < 0
    #       --p < 0
    
    #Anticlockwise +ve
    #Clockwise     -ve

    #Balancing signs

    psi = signum(x**2 + (y - R)**2 - R**2) * signum(x) * psi
    
    return (theta, psi)

#t = (theta, psi)

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

def topix(x,y):
    global size
    h = int(round(x + size[0]//2))
    k = int(round(size[1]//2 - y))
    return (h,k)


im = Image.open('A.png')
edgeim = edgeModule.edge(im)
size = edgeim.size
R = pow(size[0]**2 + size[1]**2, 0.5)/2.0
pix = edgeim.load()
x = 0
while x < size[0]:
    y = 0
    while y < size[1]:
        t,p = abc(tocart(x,y))
        if (not -90 <= t <= 90) or (not -90 <= p <= 90):
            pix[x,y] = 0
        y+=1
    print x
    x+=1
pathim = pathModule.impath(edgeim)
print pathim

cmd = []


