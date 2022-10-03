import cv2
import cvzone
from cvzone.SelfiSegmentationModule import SelfiSegmentation
import os


def blurBackground(img, value):
    segmentor = SelfiSegmentation()
    blurred = cv2.GaussianBlur(img, (value, value), 0)
    imgOut = segmentor.removeBG(img, blurred, threshold=0.7)
    return imgOut
