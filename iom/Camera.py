import cv2
import urllib.request
import numpy as np
import ssl
import logging

logging.basicConfig(filename='log.log',
                    level=logging.DEBUG,
                    format='%(asctime)s | %(name)s | %(levelname)s | %(module)s | %(lineno)d | %(message)s',
                    encoding="utf-8")

class Camera:
    def __init__(self):
        pass

    def raspCamera(self):
        pass

    def phoneCamera(self, ip):
        logging.info('start camera ...')
        url = f"https://{ip}:8080/shot.jpg"
        while True:
            gcontext = ssl.SSLContext()
            imgPath = None
            try :
                imgPath = urllib.request.urlopen(url, context=gcontext)
            except Exception as e:
                logging.exception(e)
            imgNp = np.array(bytearray(imgPath.read()), dtype=np.uint8)
            img = cv2.imdecode(imgNp, -1)

            img = cv2.resize(img, (450, 450))
            cv2.imshow("image", img)
            if ord('q') == cv2.waitKey(1):
                return img
