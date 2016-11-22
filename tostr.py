def tostr(n):
    if n > 255 or n < 0:
        print n, 'out of range'
    else:
        return (chr(n//16 + ord('0')) + chr(n%16 + ord('0')))

for k in range(255):
    print k, '--', tostr(k)

while True:
    i = input('Enter angle:')
    print tostr(i)

