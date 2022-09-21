# gestureThreshold modificabile
# salvare le note sulla singola pagina (rendere annotations una lista tripa, ovvero pagina->annotazione->punto)
# cambiare colore per disegnare

import os
import cv2
from cvzone.HandTrackingModule import HandDetector
import numpy as np

#---------VARIABILI---------

width = 1280
height = 720
folderPath = "Slides\\"
imgCount = 0

n, m = 1, 1  # moltiplicatori per la dimensione delle slide
wSmall, hSmall = int(213*n), int(120*m)  # dimensione slide

detector = HandDetector(detectionCon=0.8, maxHands=1)

gestureThreshold = 300  # soglia sopra la quale considerare un movimento come gesture
buttonPressed = False
buttonCounter = 0
buttonDelay = 20  # delay di pressione del bottone (ovvero per quanti frame una gesture è valida prima che venga rilevata nuovamente)

smoothening = 2  # alto -> cursore lento, basso -> cursore tremolante
pLocX, pLocY = 0, 0
cLocX, cLocY = 0, 0

annotations = [[]]
annotationCounter = 0  # indice di disegno (altrimenti viene disegnata una linea tra ogni disegno)
annotationStart = False  # flag per far partire un nuovo disegno
cColor = (0, 0, 255)  # colore di disegno corrente

#---------------------------

cap = cv2.VideoCapture(0) # seleziono la webcam
cap.set(3, width) # larghezza (id=3)
cap.set(4, height) # altezza (id=4)

# prendo la lista delle immagini
pathImgs = sorted(os.listdir(folderPath), key=len)  # ordino per linghezza così non ho problemi con le decine

while True:
    # Importo le immagini
    success, img = cap.read()
    img = cv2.flip(img, 1)
    pathFullImgs = os.path.join(folderPath, pathImgs[imgCount])
    imgCurrent = cv2.imread(pathFullImgs)
    #imgCurrent = cv2.resize(imgCurrent, (width, height))  # resize a dimensione fissa

    # Rileva la mano
    hands, img = detector.findHands(img)
    cv2.line(img, (0, gestureThreshold), (width, gestureThreshold), (0, 255, 0), 5)
    cv2.rectangle(img, (width//2, height-200), (width, 200), (255, 255, 255), 2)  # ROI puntatore con mano destra

    if hands and buttonPressed==False:
        hand = hands[0]
        fingers = detector.fingersUp(hand)
        cx, cy, = hand['center']  # centro della mano
        #print(fingers)

        lmList = hand['lmList']
        # ROI per il puntatore (metà destra schermo)
        xVal = int(np.interp(lmList[8][0], [width//2, imgCurrent.shape[1]], [0, width]))
        yVal = int(np.interp(lmList[8][1], [200, height-200], [0, height]))
        indexFinger = xVal, yVal

        if cy<=gestureThreshold:
            annotationStart = False

            # Gesture 1 - sinistra (pollice)
            if fingers==[1, 0, 0, 0, 0]:
                annotationStart = False

                #print("left")
                if imgCount>0:
                    buttonPressed = True
                    imgCount -= 1

                    annotations = [[]]
                    annotationCounter = 0

            # Gesture 2 - destra (mignolo)
            if fingers==[0, 0, 0, 0, 1]:
                annotationStart = False

                #print("right")
                if imgCount<len(pathImgs)-1:
                    buttonPressed = True
                    imgCount += 1

                    annotations = [[]]
                    annotationCounter = 0

        # Gesture 3 - Puntatore (indice)
        if fingers == [0, 1, 0, 0, 0]:
            cLocX = int(pLocX + (indexFinger[0] - pLocX) / smoothening)
            cLocY = int(pLocY + (indexFinger[1] - pLocY) / smoothening)
            indexFinger = cLocX, cLocY

            cv2.circle(imgCurrent, indexFinger, 8, (0, 0, 255), cv2.FILLED)
            annotationStart = False

            pLocX, pLocY = cLocX, cLocY

        # Gesture 4 - Disegno (indice e medio)
        if fingers == [0, 1, 1, 0, 0]:
            cLocX = int(pLocX + (indexFinger[0] - pLocX) / smoothening)
            cLocY = int(pLocY + (indexFinger[1] - pLocY) / smoothening)
            indexFinger = cLocX, cLocY

            if annotationStart is False:
                annotationStart = True
                annotationCounter += 1
                annotations.append([])  # inizio un nuovo disegno

            cv2.circle(imgCurrent, indexFinger, 8, (0, 0, 255), cv2.FILLED)
            annotations[annotationCounter].append(indexFinger)

            pLocX, pLocY = cLocX, cLocY
        else:
            annotationStart = False

        # Gesture 5 - Cancella ultimo disegno (pollice, indice, medio)
        if fingers == [1, 1, 1, 0, 0]:
            if annotations:
                if annotationCounter>=0:
                    annotations.pop(-1)
                    annotationCounter -= 1
                    buttonPressed = True

    else:
        annotationStart = False

    if buttonPressed:
        buttonCounter +=1
        if buttonCounter>buttonDelay:
            buttonCounter = 0
            buttonPressed = False

    for i in range(len(annotations)):
        for j in range(len(annotations[i])):
            if j!=0:
                cv2.line(imgCurrent, annotations[i][j-1], annotations[i][j], cColor, 5)  # disegna una linea tra ogni punto

    # 2) Aggiungo la webcam nella schermata delle slide
    imageSmall = cv2.resize(img, (wSmall, hSmall))
    h, w, _ = imgCurrent.shape
    imgCurrent[0:hSmall, w-wSmall:w] = imageSmall


    cv2.imshow("Image", img)
    cv2.imshow("Presentation", imgCurrent)

    key = cv2.waitKey(1)
    if key==ord('q'):
        break

