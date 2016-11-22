import serial
from time import clock
from random import randint
import sys, os

SERIALPORT = 'COM3'
BAUDRATE = 9600
TIMEOUT = 0.001

ardready = False

"""
com.py sends commands to arduino
"""
ard = serial.Serial(SERIALPORT, BAUDRATE ,timeout = TIMEOUT)
print 'port open'


def send_command(cmd, k = None):
    
    global ard
    global ardready

    #print 'CALLED send_command(' + cmd + ')'
    
    if k == None:
        k = (len(cmd)/3)

    if len(cmd)%3 != 0:
        print 'BAD COMMAND'
        return False
    else:
        for k in range(len(cmd)):
            if cmd[k] in 'abcde' and k%3 == 0:
                continue
            elif 0 <= ord(cmd[k]) - ord('0') < 16 and k%3 != 0:
                continue
            else:
                print 'BAD COMMAND'
                return False
    
    try:
        print 'Sending:',cmd
        
        noofcmds = len(cmd)/3
        print 'k =', k

        if k*3 > 64:
            print 'limit exceed'
            k = 1


        #cmd = ''

        #for i in range(t):
            #cmd += 'abc'[randint(0,2)] + (chr(randint(0,15) + ord('0')) + chr(randint(0,15) + ord('0')))
            


        start_time = clock()

        
        if not ardready:
            rd = ard.read()
            while rd != 'e':
                rd = ard.read()
            print 'ARDUINO IS READY!'
            ardready = True


        print 'len cmd', len(cmd)
            
        if len(cmd)//3 < k:
            k = len(cmd)//3

        count = 0

        ard.write(cmd)
        print 'written to arduino:', cmd
        cmd = ''
            
        while count < k:
            rd = ard.read()
            if len(rd) > 0:
                print rd, '; order', ord(rd)
                if rd in 'abcde':
                    count += 1

                

        end_time = clock()

#        ard.close()
 #       print 'serial closed'

        print noofcmds , 'commands in' , (str(end_time - start_time) + 's') , 'given', k ,'at a time'
        return True

    except KeyboardInterrupt as e:
        print e
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
        ard.close()
        print 'serial closed from exception'

def close():
    global ard
    ard.close()
    print 'serial closed'
