import cv2
from iom.screen.Recorder import Recorder
import os
import tkinter as tk
import logging

logging.basicConfig(filename='log.log',
                    level=logging.DEBUG,
                    format='%(asctime)s | %(name)s | %(levelname)s | %(module)s | %(lineno)d | %(message)s')


class Screen:

    def __init__(self, mapper):
        self.tempAudioPath = mapper.getAudioPath()

    def showImage(self, img):
        logging.info('showing image ...')
        cv2.imshow('image', img)

    def record(self):
        logging.info('start recording ...')
        path = os.path.join(self.tempAudioPath, 'record.wav')
        main = tk.Tk()
        main.title('recorder')
        main.geometry('200x50')
        Recorder(main, path)
        main.mainloop()
        return path

    def showText(self):
        pass

    def getText(self):
        pass
