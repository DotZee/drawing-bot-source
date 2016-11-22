from PIL import Image
from math import *

size = (200,200)

im = Image.new("RGB", size , "white")
pix = im.load()
R = 200*(0.5**0.5)

def plot(cmd):

    global pix
    
    s = ''
    for k in cmd:
        s+= k
    cmd = s
    print len(s)

    pts = []


    ptr = False
    
    cur_a = 0
    last_a = 0
    cur_b = 0
    last_b = 0

    n = 0
    
    while n < len(s):

        k = s[n:n+3]
        
        if k[0] == 'c':
            if toint(k[1:3]) < 0:
                ptr = False
            else:
                ptr = True
        elif k[0] == 'a':
            last_a = cur_a
            cur_a = toint(k[1:3])
        elif k[0] == 'b':
            last_b = cur_b
            cur_b = toint(k[1:3])

        if ptr:
            pt1 = cba((last_a, last_b))
            pt2 = cba((cur_a, cur_b))
            pt1 = topix(pt1)
            pt2 = topix(pt2)
            pltline(pt1,pt2)
      
        n += 3

    im.save('plot.png')

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

def topix(pt):
    x,y = pt
    global size
    h = int(round(x + size[0]//2))
    k = int(round(size[1]//2 - y))
    return (h,k)

def toint(s):

    return (ord(s[0])-ord('0'))*16 + ord(s[1]) - ord('0') - 90
    

def pltline(pt1, pt2):

    global pix
    
    x1 , y1 = pt1
    x2 , y2 = pt2

    if x1-x2 == y1-y2 == 0:
        pix[x1,y1] = (0,0,0)
        return
    
    if abs(x1 - x2) > abs(y1-y2):

        if x1 > x2:
            x2, x1 = x1, x2
            y2, y1 = y1, y2

        m = (y2 -y1)/(x2 - x1)

        x = x1

        while x <= x2:
            y  = m*x + (y1 - m*x1)
            pix[x,y] = (0,0,0)
            x += 1
    else:

        if y1 > y2:
            x2, x1 = x1, x2
            y2, y1 = y1, y2

        m = (x2 - x1)/(y2 - y1)

        y = y1

        while y < y2:
            x = m*y + (x1 - m*y1)
            pix[x,y] = (0,0,0)
            y += 1
            
    
    

#MAIN

plot(eval(raw_input('Enter command:')))
    
