#https://www.youtube.com/watch?v=k7cVPGpnels
import cv2
import cvzone
from cvzone.SelfiSegmentationModule import SelfiSegmentation
import os

'''
cap = cv2.VideoCapture(0) #capture from webcam
cap.set(3,640) #width
cap.set(4,480) #height
segmentor = SelfiSegmentation()

while True:
    success, img = cap.read()
    #blurredBackground = cv2.blur(img, (10,10))
    blurredBackground = cv2.GaussianBlur(img,(9,9),0)

    imgOut = segmentor.removeBG(img,blurredBackground, threshold=0.7)

    imgStacked = cvzone.stackImages([img,imgOut],2,1)
    cv2.imshow("Image", imgStacked)
    cv2.waitKey(1)
'''

def blurBackground(img, value):
    blurred = cv2.GaussianBlur(img, (value, value), 0)
    imgOut = segmentor.removeBG(img, blurred, threshold=0.7)
    return imgOut

def changeBackground(img, bg):
    imgOut = segmentor.removeBG(img, bg, threshold=0.7)
    return imgOut