from math import pi, sqrt, sin, asin, cos
import Image
import serial
#from com import *
import time

s = ''

img = Image.open('A.png')
size = img.size
pix = img.load()
R = sqrt(size[0]**2 + size[1]**2)/2


#Radius of arm

# t = (x,y)
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

def plot(h,k):
    for y in range(12,-12, -1):
        for x in range(-12,13):
            if(round(h) == x and round(k) == y):
                print 'O',
            elif (fabs(x**2 + (y-R)**2 - R**2) < 3):
                print '#',
            else:
                print ' ',
        print ''

def plot(d):
    for y in range(size[1] -1, -1, -1):
        for x in range(size[0]):
            if (x,y) in d:
                print '#',
            else:
                print 'O',
        print ''


#Converts the image coordinates to cartisian coordinates
#x,y pixel coordinates, size is image size tuple
def tocart(x,y):
    global size
    h = x - ((size[0] -1)//2)
    k = ((size[1] -1)//2) - y
    return (h,k)
    

pmax = tmax = 0
pmin = tmin = 180

def update(t , p):
    global tmax; global pmax; global tmin; global pmin
    if t > tmax:
        tmax = t
        
    if t < tmin:
        tmin = t
        
    if p > pmax:
        pmax = p
        
    if p < pmin:
        pmin = p
        

def isadj(a1, a2):

    a1 = (a1[0] - 90, a1[1] - 90)
    a2 = (a2[0] - 90, a2[1] - 90)

    x1, y1 = cba(a1)
    x2, y2 = cba(a2)

    if (x1 - x2)**2 + (y1 - y2)**2 <= 2:

        return True
    else:

        return False

def simplify(cmd):

    lstcmd = ''
    k = 0
    while k < len(cmd):
        if lstcmd == cmd[k] or (not bool(cmd[k])):
            del cmd[k]
        else:
            lstcmd = cmd[k]
            k += 1
            
    return cmd

l = []

def getpathcmd(angles):
    cmd = []
    
    angles.sort()

    th = []
    ps = []

    for k in angles:
        th.append(k[0])
        ps.append(k[1])

    i = 1
    strth = th[0]
    strps = ps[0]
    lstps = ps[0]

    while i < len(th) - 1:
        if strth != th[i] or ps[i] - lstps != -1:
            
            if strth == th[i-1] and strps == ps[i-1]:
                cmd.append('a' + tostr(strth) + 'b' + tostr(strps))
                cmd.append('c' + tostr(180))
            else:
                cmd.append('a' + tostr(strth) + 'b' + tostr(strps))
                cmd.append('c' + tostr(180))
                cmd.append('a' + tostr(th[i-1]) + 'b' + tostr(ps[i-1]))
            cmd.append('c00')
            strps = ps[i]
            strth = th[i]
            

        lstps = ps[i]
        i+= 1
            

    onsur = False

    return cmd
    
        


def avg(t):
    a = 0
    for k in t:
        a += k
    return a/(float(len(t)))
    
'''    
    k = 1
    cmd.append('c00')
    cmd.append('a' + tostr(l[k][0]) + 'b' + tostr(l[k][1]))
    cmd.append('c' + tostr(180))
    
    while k < len(l):

        if round(l[k][0]) == round(l[k-1][0]) and abs(l[k][1] - l[k-1][1]) <= 1:
            k += 1
            continue
        
        if not(round(l[k][0]) == round(l[k-1][0])) or not(isadj(l[k], l[k-1])):
            if chainlen > 1:
                cmd.append('a' + tostr(l[k-1][0]) + 'b' + tostr(l[k-1][1]))
            cmd.append('c00')
            cmd.append('a' + tostr(l[k][0]) + 'b' + tostr(l[k][1]))
            cmd.append('c' + tostr(180))
            chainlen = 0

        chainlen += 1
        k += 1
    
    return cmd


    cmd = ''
    lx = ly = -100

    cmd1 = []
    for k in cmd:
        if k not in cmd1:
            cmd.append(k)

    cmd.sort()
    
    for k in l:
        if (lx-k[0]) + abs(ly - k[1]) > 10:
            print 'adding c00 as', (lx,ly) , 'breaks', k
            cmd += 'c00'
        cmd +=  'b' + tostr(k[1]) +'a' + tostr(k[0])
        lx = k[0]
        ly = k[1]
        if (lx-k[0])**2 + (ly - k[0])**2 > 3:
            cmd += 'c;4'


    return cmd
'''

def tostr(n):
    n = int(round(n))
    if n > 255 or n < 0:
        print n, 'out of range'
    else:
        return (chr(n//16 + ord('0')) + chr(n%16 + ord('0')))

def diff(l1,l2):
    return (l1[0]-l2[0])**2  + (l1[1]-l2[1])**2


# t = (x,y); psi = angle (ac +Ve)
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

def toset(l):
    t = []
    for k in l:
        if k not in t:
            t.append(k)
    t.sort()
    return t

def toint(s):
    n = 0
    while len(s) > 0:
        n = n*16 + ord(s[0]) - ord('0')
        s = s[1:]
    return n

#Main
img = Image.open('A.png')
size = img.size
pix = img.load()
R = sqrt(size[0]**2 + size[1]**2)/2


print 'size', size

'''
angles = []
points = []

tplft = (size[0] + 1 , size[1] + 1)


for x in range(size[0]):
    for y in range(size[1]):
        
        if pix[x,y] == (255,255,255):
            continue
        points.append((x,y))
        ang = abc(tocart(x,y))
        ang = (int(round(ang[0] + 90)), int(round(ang[1] + 90)))
        
        if ang not in angles:
            angles.append(ang)
            
        if x**2 + y**2 < tplft[0]**2 + tplft[1]**2:
            tplft = (x,y)

'''

#get angles!

cmd = getpathcmd(angles)

cmd = simplify(cmd)
print cmd

d = []

for s in cmd:
    if len(s) > 4:
        t = toint(s[1:3]) - 90
        p = toint(s[4:]) - 90
        x,y = cba((t,p))
        x = int(round(x) + size[0]//2)
        y = int(round(y) + size[1]//2)
        d.append((x,y))
print 'd:',d 
plot(d)

est = len(cmd)*1.63

print 'EST:', str(int(est//60)) + 'min', str(int(round(est%60))) + 's'

d = []


for k in cmd:
    send_command(k)
    time.sleep(1)

close()





'''


angles = []
points = []
outofrange = []

for y in range(size[1]):
    for x in range(size[0]):
        if min(pix[x,y]) < 128:
           points.append(tocart(x,y))

for k in points:
    i = abc(k[0],k[1])
    i = (int(round(i[0]+90)),int(round((i[1]+90))))
    if not(0 <= i[0] <= 180 and 0 <= i[1] <= 180):
        outofrange.append(i)
    else:
        angles.append(i)

cmd = getpathcmd(angles)

if send_commands(cmd):
    raw_input("Commands Incomplete :(")
else:
    raw_input('Commands completed!')


'''
