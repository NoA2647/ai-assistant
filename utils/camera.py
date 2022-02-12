import cv2
import urllib.request
import numpy as np
import re

WORDS = ["camera"]  # format: open camera by ?

PRIORITY = 3


def run(command, speaker, profile, mapper):
    ip = command.split(" ")[-1]
    url = f"http://{ip}:8080/shot.jpg"
    while True:
        imgPath = urllib.request.urlopen(url)
        imgNp = np.array(bytearray(imgPath.read()), dtype=np.uint8)
        img = cv2.imdecode(imgNp, -1)

        img = cv2.resize(img, (450, 450))
        cv2.imshow("image", img)
        if ord('q') == cv2.waitKey(1):
            exit(0)


def isValid(command):
    return bool(re.search(r'\bcamera\b', command, re.IGNORECASE))
