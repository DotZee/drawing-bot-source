from com import *
import time

def tostr(n):
    n = int(round(n))
    if n > 255 or n < 0:
        print n, 'out of range'
    else:
        return (chr(n//16 + ord('0')) + chr(n%16 + ord('0')))

def loop(pts, itr = 1):
    try:
        k = 0
        while itr > 0:
            cmd = 'a' + tostr(pts[k][0]) + 'b' + tostr(pts[k][1])
            print 'writing', cmd
            send_command(cmd)
            time.sleep(5)
            itr -= 1
            k = (k+1)%len(pts)
            print 'itr', itr
    except Exception as e:
        print 'exception!!', e
        ard.close()
        return False
    else:
        return True

print '(1,2), (3,2) sets arm to 1 and rotor to 2 then after 5sec ...'

t = eval('[' + raw_input('Enter angles:') + ']')
itr = input('iterations')
try:
    while loop(t,itr):
        t = eval('[' + raw_input('Enter angles:') + ']')
        itr = input('iterations')
except:
    pass
finally:
    ard.close()
