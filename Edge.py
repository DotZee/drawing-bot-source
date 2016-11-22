from PIL import Image
from math import sqrt
import time

#DEBUG CODE
#a = Image.open('A.png'); e = edge(a); e.save('edge2.png')

swtchr = {0:(-1,-1), 1:(0,-1), 2:(1,-1), 3:(1,0),
            4:(1,1), 5:(0,1), 6:(-1,1), 7:(-1,0)}

invswt = dict(zip(swtchr.values(), swtchr.keys()))

def edge(im, MAXDEV = 1.73*255/8):

    start_time = time.clock()
    
    size = im.size
    pix = im.load()
    
    out = Image.new('1', size, color = 1)
    opix = out.load()

    x = 1

    clr = pix[0,0]

    tempim = im.copy()

    tempix = tempim.load()

    y = 1
    while x < size[0] - 1:
        while y < size[1] - 1:
            n = 0
            for k in range(8):
                cfx, cfy = swtchr[k]

                if 0 <= x + cfx < size[0] and 0 <= y + cfy < size[1]:
                    if min(diff(pix[x,y], pix[x+cfx,y+cfy])) <= MAXDEV:
                        n+=1
                    else:

                        #if avg(pix[x,y]) < 100:
                            #print (x,y), (x+cfx, y+cfy), 'REJECTED',
                            #print pix[x,y], pix[x+cfx,y+cfy]
                        
                        clr = pix[x+cfx, y+cfy]
                    
            #if avg(pix[x,y]) < 100:
                #print (x,y),':', n
            
            if 0 < n <= 4:
                opix[x,y] = 0
                tempix[x,y] = clr
            
            y += 1
            
        y = 0
        x += 1

    
    im = tempim.copy()
    del tempix, tempim, pix
    
    #im.save('remaining.png')
    #out.save('edge1.png')
    
    pix  = im.load()
    
    x = 0

    while x < size[0] - 1:
        y = 0
        while y < size[1] - 1:
            clr = pix[x,y]
            cl2 = pix[x+1, y]
            cl3 = pix[x, y+1]
            cl4 = pix[x+1,y+1]

            if max(diff(clr,cl2,cl3,cl4)) > MAXDEV:
                opix[x,y] = 0
            
            y += 1
        x += 1

    end_time = time.clock()

    print 'computed edges in', str(round(end_time-start_time, 3))+'s'
    
    return out

def diff(cl1, *cl):
    d = []
    
    for clr in cl:
        d.append(0)
        
        for k in range(len(cl1)):
            d[-1] += (cl1[k] - clr[k])**2
                
        d[-1] = sqrt(d[-1])
    
    return d


def avg(t):
    a = 0
    for k in t:
        a += k
    return a/float(len(t))

#Remove the part below if you don't wish to debug!
