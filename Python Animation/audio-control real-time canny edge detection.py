import numpy as np
import random
import cv2
import pyaudio
from math import sin

# audio setup
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
RECORD_SECONDS = 20
p = pyaudio.PyAudio()
stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)

# video setup
cap = cv2.VideoCapture(0)

while True:
    # Read video frame
    ret, frame = cap.read()

    # Read audio data
    data = stream.read(CHUNK)
    numpydata = np.frombuffer(data, dtype=np.int16) * 1.0
    am = int(np.mean(numpydata ** 2) ** (1/2.5))

    # Display the original video frame
    cv2.imshow('inputframe', frame)

    # Apply Canny edge detection to the frame
    edges = cv2.Canny(frame, am, 250)

    # Convert the edges to RGB and add random color
    rgb = cv2.cvtColor(edges, cv2.COLOR_GRAY2RGB)
    random_color = np.array((random.random(), random.random(), random.random()), np.float16)
    rgb = (rgb * random_color).astype("uint8")

    # Flip the image horizontally
    flip_img = cv2.flip(rgb, 1)

    # Display the mirrored image
    cv2.imshow("Mirrored Image", flip_img)

    # Display the edges in color
    cv2.imshow('edges', rgb)

    # Display original and mirrored images side by side
    im_v = cv2.hconcat([rgb, flip_img])
    cv2.imshow("Mirror side by side", im_v)

    # Check for the 'Esc' key to exit the loop
    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break

# Release resources
cap.release()