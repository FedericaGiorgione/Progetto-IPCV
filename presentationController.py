# https://www.youtube.com/watch?v=CKmAZss-T5Y 26:23

import os
import cv2

#---------VARIABILI---------

width = 1280
height = 720
folderPath = "Slides\\"
imgCount = 0
n, m = 1, 1  # moltiplicatori per la dimensione delle slide
wSmall, hSmall = int(213*n), int(120*m)  # dimensione slide

#---------------------------

cap = cv2.VideoCapture(0) # seleziono la webcam
cap.set(3, width) # larghezza (id=3)
cap.set(4, height) # altezza (id=4)

# prendo la lista delle immagini
pathImgs = sorted(os.listdir(folderPath), key=len)  # ordino per linghezza così non ho problemi con le decine

while True:
    # 1) Importo le immagini
    success, img = cap.read()
    pathFullImgs = os.path.join(folderPath, pathImgs[imgCount])
    imgCurrent = cv2.imread(pathFullImgs)
    imgCurrent = cv2.resize(imgCurrent, (width, height))

    # 2) Aggiungo la webcam nella schermata delle slide
    imageSmall = cv2.resize(img, (wSmall, hSmall))
    h, w, _ = imgCurrent.shape
    imgCurrent[0:hSmall, w-wSmall:w] = imageSmall


    cv2.imshow("Image", img)
    cv2.imshow("Presentation", imgCurrent)

    key = cv2.waitKey(1)
    if key==ord('q'):
        break

