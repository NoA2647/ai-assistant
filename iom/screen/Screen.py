import cv2
from iom.screen.Recorder import Recorder
import os
import tkinter as tk


class Screen:

    def __init__(self, mapper):
        self.tempAudioPath = mapper.getAudioPath()

    def showImage(self, img):
        cv2.imshow('image', img)

    def record(self):
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
