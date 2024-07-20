import cv2
import numpy as np
import matplotlib.pyplot as plt

img = cv2.imread('test_black_stripes.PNG')

img_grey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
contrast = img_grey.std()

img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
saturation = img_hsv[:, :, 1].mean()
fm = cv2.Laplacian(img_grey, cv2.CV_64F).var()
print("contrast is: "+str(contrast))
print("saturation is: "+str(saturation))
print("Sharpness is: "+str(fm))
cv2.imshow('image',img)
cv2.waitKey(0)
cv2.destroyAllWindows()
