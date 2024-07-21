import cv2
import numpy as np
import matplotlib.pyplot as plt
from numpy.linalg import norm
from time import sleep
import time
import keyboard
from pythonosc import udp_client
import socket
from webcolors import rgb_to_name
import webcolors
from collections import defaultdict

ip = socket.gethostbyname(socket.gethostname())
port = 4560
client = udp_client.SimpleUDPClient(ip, port)

camera = cv2.VideoCapture(0)#b,g,r = cv2.split(image)
import math

KNOWN_COLORS = {
    'black': (0, 0, 0),
    'white': (255, 255, 255),
    'red': (255, 0, 0),
    'green': (0, 255, 0),
    'blue': (0, 0, 255),
    'yellow': (255, 255, 0),
    'cyan': (0, 255, 255),
    'magenta': (255, 0, 255),
    'gray': (128, 128, 128),
}

known_colors_rgb = np.array(list(KNOWN_COLORS.values()))
color_names = list(KNOWN_COLORS.keys())

def closest_color(requested_color):
    # Berechnung der Distanz für alle bekannten Farben
    diffs = np.sum((known_colors_rgb - requested_color) ** 2, axis=1)
    closest_index = np.argmin(diffs)
    return color_names[closest_index]

def color_count(image_array):
    # Umwandlung des Bildarrays in ein zweidimensionales Array (Pixel x Kanäle)
    pixels = image_array.reshape(-1, image_array.shape[-1])
    
    # Zähler für die Farben
    color_counter = defaultdict(int)
    
    # Bestimmen des Farbnamen für jedes Pixel und Erhöhen des Zählers
    for pixel in pixels:
        color_name = closest_color(pixel)
        color_counter[color_name] += 1
    
    return color_counter

def most_common_color_name(image_array):
    color_counts = color_count(image_array)
    
    # Finden des am häufigsten vorkommenden Farbnamen
    most_common = max(color_counts, key=color_counts.get)
    
    return most_common
def brightnesszwischenwert(img):
    imghsv = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
    return cv2.mean(imghsv)[2:3][0]

def unique_count_app(a):
    colors, count = np.unique(a.reshape(-1,a.shape[-1]), axis=0, return_counts=True)
    return colors[count.argmax()]

def Werte_printen():
    result, image = camera.read()
    height, width = frame.shape[:2]
    dominant_color = most_common_color_name(image)
    brightness = round(brightnesszwischenwert(image)*(127/255))
    img_grey = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    contrastzwischenwert = img_grey.std()
    img_hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    saturationzwischenwert = img_hsv[:, :, 1].mean()
    saturation = round(saturationzwischenwert*(127/255))
    sharpnesszwischenwert = cv2.Laplacian(img_grey, cv2.CV_64F).var()
    sharpness = round(np.clip((sharpnesszwischenwert / 1000) * 127, 1, 127))
    contrast = round(max(0, min(127,contrastzwischenwert)))
    client.send_message('/bilddaten', f"dominant_color:{str(dominant_color)}")
    client.send_message('/bilddaten', f"brightness:{str(brightness)}")
    client.send_message('/bilddaten', f"contrast:{str(contrast)}")
    client.send_message('/bilddaten', f"saturation:{str(saturation)}")
    client.send_message('/bilddaten', f"sharpness:{str(sharpness)}")

while True:
    timeout = time.time() + 5   # 5 minutes from now
    #cv2.imshow('image',image)
    while(camera.isOpened()):
        if keyboard.is_pressed('q'):  # if key 'q' is pressed 
            raise SystemExit # finishing the loop

        if  time.time() > timeout:
            Werte_printen()
            timeout = time.time() + 5
        ret, frame = camera.read()
        if ret == True:
            
    # Display the resulting frame
            cv2.imshow('Frame',frame)
 
    # Press Q on keyboard to  exit
            if cv2.waitKey(25) & 0xFF == ord('q'):
                break
 
  # Break the loop
        else: 
            break


