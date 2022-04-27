import cv2


class Screen:
    def __init__(self):
        pass

    def show(self, img):
        cv2.imshow('image', img)
