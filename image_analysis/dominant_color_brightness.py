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


print("dominant_color: "+str(unique_count_app(image)))

#average brightness of an image
def brightness(img):
    imghsv = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
    return cv2.mean(imghsv)[2:3][0]

print("brightness: "+str(brightness(image)))


img_grey = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
contrast = img_grey.std()

img_hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
saturation = img_hsv[:, :, 1].mean()
fm = cv2.Laplacian(img_grey, cv2.CV_64F).var()
print("contrast: "+str(contrast))
print("saturation: "+str(saturation))
print("Sharpness: "+str(fm))
cv2.imshow('image',image)
cv2.waitKey(0)
cv2.destroyAllWindows()



