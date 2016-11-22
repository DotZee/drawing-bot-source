from math import *
from PIL import Image
import time

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

def transform(t , psi):
    x1,y1 = t
    x = x1*cos(pi*psi/180) + y1*sin(pi*psi/180)
    y = -x1*sin(pi*psi/180) + y1*cos(pi*psi/180)
    return (x,y)

def cba(t):
    
    theta, psi = t
    
    x1 = R*sin(pi*theta/180)
    y1 = R*(1-cos(pi*theta/180))

    return transform((x1,y1), psi)

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

def signum(x):
    if x < 0:
        return -1
    elif x > 0:
        return 1
    else:
        return 0




start = time.clock()

im = Image.new('RGB', (181,181))
pix = im.load()
size = im.size

R = pow(size[0]**2 + size[1]**2, 0.5)/2.0

inv = []

th = -90
while th <= 90:
    ps = -90
    while ps <= 90 and ps - th < 90 and th != 0:
        x,y = cba((th,ps))
        x = round(x,4)
        y = round(y,4)

        if (x,y) in inv:
            pix[topix(th,ps)] = (0,255,0)
        else:
            inv.append((x,y))
            pix[topix(th,ps)] = (255,0,0)
        
        ps+=1
    th += 1

im.save('gr.png')

end = time.clock()

print end - start
