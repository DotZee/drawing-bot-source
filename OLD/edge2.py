import cv2

im = cv2.imread('A.png')

edge = cv2.Canny(im, input('Minimum Thresh:\t'), input('Maximum Thresh:\t'))

cv2.imwrite('edge.png', edge)
