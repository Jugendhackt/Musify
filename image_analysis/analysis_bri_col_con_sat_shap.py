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
#b,g,r = cv2.split(image)


def unique_count_app(a):
    colors, count = np.unique(a.reshape(-1,a.shape[-1]), axis=0, return_counts=True)
    return colors[count.argmax()]


dominant_color = unique_count_app(image)

#average brightness of an image
def brightnesszwischenwert(img):
    imghsv = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
    return cv2.mean(imghsv)[2:3][0]

brightness = round(brightnesszwischenwert(image)*(127/255))



img_grey = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
contrastzwischenwert = img_grey.std()

img_hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
saturationzwischenwert = img_hsv[:, :, 1].mean()
saturation = round(saturationzwischenwert*(127/255))
sharpnesszwischenwert = cv2.Laplacian(img_grey, cv2.CV_64F).var()#
sharpness = round((max(300, min(1500,sharpnesszwischenwert))-300)*(127/1200))
contrast = round(max(0, min(127,contrastzwischenwert)))

for i in range(0,len(dominant_color)):
    dominant_color[i] = round(dominant_color[i]*(127/255)) 

print("dominant_color: "+str(dominant_color))
print("brightness: "+str(brightness))
print("contrast: "+str(contrast))
print("saturation: "+str(saturation))
print("Sharpness: "+str(sharpness))
cv2.imshow('image',image)
#cv2.waitKey(0)
cv2.destroyAllWindows()




