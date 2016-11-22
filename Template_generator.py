from math import *
from PIL import Image

R = 0

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


a = input('For template of dimensions (a, a), a is in pixels\nEnter a: ')
R = (a/2)*sqrt(2)
size = (a,a)
temp = Image.new(mode = 'RGB', size = (a,a), color = 'WHITE')
pix = temp.load()

theta = 0
while theta <= 90:
    psi = -90
    
    while psi <= 90:
        try:
            x,y = topix(*cba((theta, psi)))
            pix[x,y] = (0,0,0)
        except IndexError:
            pass
        finally:
            psi += 180
    
    theta += 1

temp.save('template.png')
