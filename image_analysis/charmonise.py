#
#  Use k-means clustering to find the most-common colors in an image
#
import cv2
import numpy as np
import sklearn
from sklearn.cluster import KMeans


def make_histogram(cluster):
    """
    Count the number of pixels in each cluster
    :param: KMeans cluster
    :return: numpy histogram
    """
    numLabels = np.arange(0, len(np.unique(cluster.labels_)) + 1)
    hist, _ = np.histogram(cluster.labels_, bins=numLabels)
    hist = hist.astype('float32')
    hist /= hist.sum()
    return hist


def make_bar(height, width, color):
    """
    Create an image of a given color
    :param: height of the image
    :param: width of the image
    :param: BGR pixel values of the color
    :return: tuple of bar, rgb values, and hsv values
    """
    bar = np.zeros((height, width, 3), np.uint8)
    bar[:] = color
    red, green, blue = int(color[2]), int(color[1]), int(color[0])
    hsv_bar = cv2.cvtColor(bar, cv2.COLOR_BGR2HSV)
    hue, sat, val = hsv_bar[0][0]
    return bar, (red, green, blue), (hue, sat, val)


def sort_hsvs(hsv_list):
    """
    Sort the list of HSV values
    :param hsv_list: List of HSV tuples
    :return: List of indexes, sorted by hue, then saturation, then value
    """
    bars_with_indexes = []
    for index, hsv_val in enumerate(hsv_list):
        bars_with_indexes.append((index, hsv_val[0], hsv_val[1], hsv_val[2]))
    bars_with_indexes.sort(key=lambda elem: (elem[1], elem[2], elem[3]))
    return [item[0] for item in bars_with_indexes]


# START HERE
img_original = cv2.imread('C:/Users/janwi/OneDrive/Desktop/flag.jpg')
down_points = (200,200)
img = cv2.resize(img_original, down_points, interpolation= cv2.INTER_LINEAR)
height, width, _ = np.shape(img)

# reshape the image to be a simple list of RGB pixels
image = img.reshape((height * width, 3))
# we'll pick the 5 most common colors
num_clusters = 5
clusters = KMeans(n_clusters=num_clusters)
clusters.fit(image)
# count the dominant colors and put them in "buckets"
histogram = make_histogram(clusters)
# then sort them, most-common first
combined = zip(histogram, clusters.cluster_centers_)
combined = sorted(combined, key=lambda x: x[0], reverse=True)

# finally, we'll output a graphic showing the colors in order
bars = []
hsv_values = []
rgb_values = []
h_val = []
for index, rows in enumerate(combined):
    bar, rgb, hsv = make_bar(100, 100, rows[1])
    #print(f'Bar {index + 1}')
    #print(f'  RGB values: {rgb}')
    #print(f'  HSV values: {hsv}')
    hsv_values.append(hsv)
    if hsv[0] < 255/2:
        h_val.append(hsv[0])
    else:
        h_val.append(round(hsv[0]-255/2))
    rgb_values.append(rgb)
    bars.append(bar)

#------ CUSTOM CODE STARTS HERE -------
h_val = list(set(h_val))
h_val.sort()
span = 0
for i in range(0,len(h_val)-1):
    span += abs(h_val[i+1] - h_val[i])
span += abs(h_val[-1] - h_val[0])
span = 2.5*(span/(len(hsv_values)))
span = np.clip(span, 0, 127)
print("Simple hue-distance separation of dominant color: "+str(span))

# sort the bars[] list so that we can show the colored boxes sorted
# by their HSV values -- sort by hue, then saturation
sorted_bar_indexes = sort_hsvs(hsv_values)
sorted_bars = [bars[idx] for idx in sorted_bar_indexes]

#cv2.imshow('Sorted by HSV values', np.hstack(sorted_bars))
cv2.imshow(f'{num_clusters} Most Common Colors', np.hstack(bars))
cv2.waitKey(0)
