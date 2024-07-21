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
import rtmidi

ip = socket.gethostbyname(socket.gethostname())
port = 4560
client = udp_client.SimpleUDPClient(ip, port)


# Midi Client

midiout = rtmidi.MidiOut()
available_ports = midiout.get_ports()
print(available_ports)

if available_ports:
    midiout.open_port(1) # loopMIDI Port 1 (zweiter Port im Array)
else:
    midiout.open_virtual_port("My virtual output")

MIDI_CC_23 = 23
MIDI_CC_24 = 24
MIDI_CC_25 = 25
MIDI_CC_26 = 26
MIDI_CC_37 = 37

camera = cv2.VideoCapture(0)#b,g,r = cv2.split(image)
import math

KNOWN_COLORS = {
    'black': (0, 0, 0),
    'white': (255, 255, 255),
    'red': (0, 0, 255),
    'green': (0, 255, 0),
    'blue': (255, 0, 0),
    'yellow': (0, 255, 255),
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
    image_downsized = cv2.resize(image_array, (200,200), interpolation=cv2.INTER_LINEAR)
    color_counts = color_count(image_downsized)
    
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
    #image = cv2.imread("C:/Users/localadmin/Downloads/Landschaftsbild-201020572812.jpg")
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
    print("______________________")
    client.send_message('/bilddaten', f"dominant_color:{str(dominant_color)}")
    # midiout.send_message([0xB0, MIDI_CC_23, dominant_color])
    print(f"dominant_color:{str(dominant_color)}")
    client.send_message('/bilddaten', f"brightness:{str(brightness)}")
    midiout.send_message([0xB0, MIDI_CC_24, brightness])
    print(f"brightness:{str(brightness)}")
    client.send_message('/bilddaten', f"contrast:{str(contrast)}")
    midiout.send_message([0xB0, MIDI_CC_25, contrast])
    print(f"contrast:{str(contrast)}")
    client.send_message('/bilddaten', f"saturation:{str(saturation)}")
    midiout.send_message([0xB0, MIDI_CC_26, saturation])
    print(f"saturation:{str(saturation)}")
    client.send_message('/bilddaten', f"sharpness:{str(sharpness)}")
    midiout.send_message([0xB0, MIDI_CC_37, sharpness])
    print(f"sharpness:{str(sharpness)}")

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


