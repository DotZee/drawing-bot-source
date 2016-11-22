from math import pi, sqrt, sin, asin, cos
import Edge as edgemodule
import path as pathmodule
import Image
import serial
import time

DEBUG =False

MAXCMDLEN = 20

ALREADY_EDGE = True
SHOW = True
SECONDONLY = False

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

def topix(x,y):
    global size
    h = int(round(x + size[0]//2))
    k = int(round(size[1]//2 - y))
    return (h,k)

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
            try:
                t, p = abc(tocart(*pathpts[i][j]))
            except:
                if abc(tocart(*pathpts[i][j])) == None:
                    print "out of range"
                else:
                    print 'something fishy'
                continue
            
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
                cmd.append('d' + tostr(50) +'c' + tostr(180))
                firstcmd = False
            

        cmd.append('c00' + 'd' + tostr(50))

    maxcmdlen = 0
    
    for k in range(len(cmd)):
        
        if 'd' in cmd[k][-3:]:
            cmd[k] = cmd[k][:-3]
            print cmd[k]
            
        if len(cmd[k]) > maxcmdlen:
            maxcmdlen = len(cmd[k])


    while '' in cmd:
        cmd.remove('')
    
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

def outofrange(x,y):
    global size
    if abc(tocart(x,y)) == None:
        return True
    else:
        return False

def avg(seq):
    try:
        s = 0
        
        for a in seq:
            s += a

        return s/len(seq)
    except:
        return seq
    
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



#--------MAIN--------

img = Image.open('A.png').convert('1')

if not ALREADY_EDGE:
    img = edgemodule.edge(img)

size = img.size
R = (size[0]**2 + size[1]**2)**(0.5)/2
img2 = Image.new('1', size, color = 1)


pix = img.load()
pix2 = img2.load()
x = 0
while x < size[0]:
    y = 0
    while y < size[1]:

        if pix[x,y] < 128 and outofrange(x,y):

            pix2[x,y] = 0
            pix[x,y] = 1
            
        y+=1
    x+=1

img2 = img2.rotate(180)

img.save('1.png')
img2.save('2.png')

cmd1 = ''

est = 0

path = pathmodule.impath(img, SHOW)

print 'path length:' , len(path)

cmd = pathedgecmd(path)

for k in cmd:
    if 'd' in k:
        est += 0.16
    
est += len(cmd)*1.01

print "Command length:", len(cmd)
print 'Estimated', str(int(est/60)) + 'm', str(int(est%60)) + 's'

print cmd

if not (SECONDONLY or DEBUG):
    
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
        raise ValueError('Program Terminated')
    else:
        send_command('a' + tostr(60) + 'c00')
test = est
est = 0

path = pathmodule.impath(img2, SHOW)

print 'path length:' , len(path)

cmd = pathedgecmd(path)

for k in cmd:
    if 'd' in k:
        est += 0.16
    
est += len(cmd)*1.01

print "Command length:", len(cmd)
print 'Estimated', str(int(est/60)) + 'm', str(int(est%60)) + 's'

print cmd

if not DEBUG:
    
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
        print 'Program Terminated'
    else:
        send_command('a' + tostr(60) + 'c00')
    finally:
        ard.close()


if DEBUG:
    raw_input('Enter to close')
