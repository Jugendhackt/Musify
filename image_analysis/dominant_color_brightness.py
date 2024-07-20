import cv2
import numpy as np
import matplotlib.pyplot as plt
from numpy.linalg import norm


# for opening the picture
#
# img = cv2.imread('Bild.jpg')
# cv2.imshow('image',img)
# cv2.destroyAllWindows()
# pixel = image[200, 250]

image = cv2.imread("Bild.jpg")

#dominant_color = unique_count_app(image)
def unique_count_app(a):
    colors, count = np.unique(a.reshape(-1,a.shape[-1]), axis=0, return_counts=True)
    return colors[count.argmax()]


#average brightness of an image
def brightness(img):
    imghsv = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
    return cv2.mean(imghsv)[2:3][0]

#print(brightness(image))


cv2.waitKey(0)