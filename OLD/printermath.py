from math import pi, sqrt, sin, asin, cos
import Edge as edgemodule
import path as pathmodule
import Image
import serial
import time


MAXCMDLEN = 20

ALREADY_EDGE = True
SHOW = True

s = ''


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

    
    if abs(theta) > 60 or abs(psi) > 90:
        print 'OUT OF RANGE', t, (round(theta), round(psi))
    
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

    im2 = Image.new('RGB', size)
    pix2 = im2.load()

    
    for y in range(size[1] -1, -1, -1):
        for x in range(size[0]):
            if (x,y) in d:
                pix2[x,y] = (154,153,184)
            
    im2.save('out.png')


#Converts the image coordinates to cartisian coordinates
#x,y pixel coordinates, size is image size tuple
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

#if real is True then returns the actual real world distance between points
#Approximately in cm
def dist(ang1, ang2, real = True):
    ang1 = (ang1[0]-90, ang1[1]-90)
    ang2 = (ang2[0]-90, ang2[1]-90)
    x1,y1 = cba(ang1)
    x2,y2 = cba(ang2)
    s = sqrt((x1-x2)**2 + (y1-y2)**2)
    if real:
        return s*12/(R*1.41421)
    else:
        return

def getpathcmd(angles):
    cmd = []
    l = []
    l.append([angles[0]])

    i = 1
    
    while i < len(angles):
        if angles[i-1][0] != angles[i][0] or abs(angles[i][1] - angles[i-1][1]) > 1:
            l[-1].append(angles[i-1])
            l.append([angles[i]])
        i += 1
    l[-1].append(angles[-1])
    
    i = 0

    #print l
    
    while i < len(l):

        cmd.append('c00')
        cmd.append('a' + tostr(l[i][0][0]) + 'b' + tostr(l[i][0][1]))
        cmd.append('c' + tostr(180))
        
        if l[i][0] != l[i][1]:
            cmd.append('a' + tostr(l[i][1][0]) + 'b' + tostr(l[i][1][1]))

        i += 1
    
    return cmd
    

def pathedgecmd(pathpts):

    
    pathangles = [[]]

    #print 'pathpts', pathpts

    for i in range(len(pathpts)):
        for j in range(len(pathpts[i])):
            
            t, p = abc(tocart(*pathpts[i][j]))
            
            t = 90 + int(round(t)); p = 90 + int (round(p))

            if len(pathangles[-1]) > 0 and pathangles[-1][-1] == (t,p):
                continue


            if len(pathangles[-1]) > 0 and ((abs(pathangles[-1][-1][0] - t) > 5 or abs(pathangles[-1][-1][1] - p) > 5)) and (dist(pathangles[-1][-1], (t,p)) > 0.5 or (abs(pathangles[-1][-1][0] - t) > 10 or abs(pathangles[-1][-1][1] - p) > 20)):
                
                pathangles.append([])

            pathangles[-1].append((t,p))

        pathangles.append([])

    while [] in pathangles:
        pathangles.remove([])

    cmd = ['c' + tostr(00),'']

    for k in pathangles:

        firstcmd = True
        
        for pt in k:
            
            if len(cmd[-1]) > 15:
               cmd.append('')
               
            cmd.append('a' + tostr(pt[0]) + 'b' + tostr(pt[1]))

            if firstcmd:
                cmd.append('c' + tostr(180))
                firstcmd = False
            

        cmd.append('c00')

    maxcmdlen = 0
    
    for k in range(len(cmd)):
        
        if 'd' in cmd[k][-3:]:
            #print 'changing', cmd[k], 'to',
            cmd[k] = cmd[k][:-3]
            print cmd[k]
            
        if len(cmd[k]) > maxcmdlen:
            maxcmdlen = len(cmd[k])


    while '' in cmd:
        cmd.remove('')
    
    #print cmd
    #print 'length =' , len(cmd)
    #print 'max cmd len = ', maxcmdlen

    return timecutter(cmd)


def timecutter(cmd):

    k = 0

    while k < len(cmd)-1:

        if len(cmd[k]) + len(cmd[k+1]) <= MAXCMDLEN - 3:
            cmd[k] = cmd[k] + 'd10' + cmd[k+1]
            del cmd[k+1]
        else:
            k += 1

    return cmd
    


def avg(t):
    a = 0
    for k in t:
        a += k
    return a/(float(len(t)))
    

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

def tomin(t):
    return str(int(t/60)) + 'm ' + str(t%60) + 's'

#Main


for k in range(2):
    
    img = Image.open('A.png')
    
    if k == 1:
        img = img.rotate(180)
        
    size = img.size
    img.paste(1,(size[0]//2, 0,size[0],size[1]))
    pix = img.load()
    R = sqrt(size[0]**2 + size[1]**2)/2
    est = 0

    if ALREADY_EDGE:
        edge = img
    else:
        edge = edgemodule.edge(img)
        edge.save('edge.png')
        
    path = pathmodule.impath(edge, SHOW)

    print 'path length:' , len(path)

    cmd = pathedgecmd(path)

    for k in cmd:
        if 'd' in k:
            est += 0.16
        
    est += len(cmd)*1.01

    print "Command length:", len(cmd)
    print 'Estimated', str(int(est/60)) + 'm', str(int(est%60)) + 's'

    print cmd

'''
    from com import *

    try:
        start_time = time.clock()
        for k in cmd:
            #print 'send', k
            if not send_command(k):
                print 'BAD COMMANDS GIVEN!!'
                raise NameError('BAD COMMAND')
            tm = time.clock()
            print 'Elaspsed:', tomin(tm - start_time)
            print 'Left:', tomin(est + start_time  - tm)
            #time.sleep(1)
    except KeyboardInterrupt as e:
        print e
        ard.close()
'''
'''
size = img.size
pix = img.load()
R = sqrt(size[0]**2 + size[1]**2)/2
est = 0

if ALREADY_EDGE:
    edge = img
else:
    edge = edgemodule.edge(img)
    edge.save('edge.png')
    
path = pathmodule.impath(edge, False)

print 'path length:' , len(path)

cmd = pathedgecmd(path)

for k in cmd:
    if 'd' in k:
        est += 0.16
    
est += len(cmd)*1.01

print "Command length:", len(cmd)
print 'Estimated', str(int(est/60)) + 'm', str(int(est%60)) + 's'

print cmd


from com import *

try:
    start_time = time.clock()
    for k in cmd:
        #print 'send', k
        if not send_command(k):
            print 'BAD COMMANDS GIVEN!!'
            raise NameError('BAD COMMAND')
        tm = time.clock()
        print 'Elaspsed:', tomin(tm - start_time)
        print 'Left:', tomin(est + start_time  - tm)
        #time.sleep(1)
except KeyboardInterrupt as e:
    print e
    ard.close()

'''


'''
print 'size', size

#get angles!
angles = []

th = 0
ps = 0



while th <= 180:
    while ps <= 180 and ps - th < 90 and th != 0:
        
        x,y = cba((th-90, ps-90))

        x,y = topix(x,y)

        if 0 <= x < size[0] and 0 <= y < size[1]:
            if avg(pix[x,y]) < 250:
                angles.append((th,ps))
        
        ps += 1
        
    th += 1
    ps = 0

cmd = getpathcmd(angles)

cmd = simplify(cmd)
print cmd

d = []

for s in cmd:
    if len(s) > 4:
        t = toint(s[1:3]) - 90
        p = toint(s[4:]) - 90
        print t+90,p+90
        x,y = cba((t,p))
        x = int(round(x + size[0]//2))
        y = int(round(y + size[1]//2))
        d.append((x,y))


print 'd:',d

plot(d)

est = len(cmd)*1.5

print 'EST:', str(int(est//60)) + 'min', str(int(round(est%60))) + 's'

d = []


for k in cmd:
    send_command(k)
    time.sleep(1)

close()
'''
