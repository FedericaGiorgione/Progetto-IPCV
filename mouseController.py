# prima va identificata la faccia

import cv2
import numpy as np
import HandTrackingModule as htm  # mediapipe per il tracking della mano
import time
import autopy  # per muovere il mouse

#---------VARIABILI---------

wCam = 1280
hCam = 720
roiDim = 200
smoothening = 4  # alto -> cursore lento, basso -> cursore tremolante

#---------------------------


cap = cv2.VideoCapture(0) # seleziono la webcam
cap.set(3, wCam) # larghezza (id=3)
cap.set(4, hCam) # altezza (id=4)

pTime = 0 # past time

pLocX, pLocY = 0, 0
cLocX, cLocY = 0, 0

detector = htm.handDetector(maxHands=1)

wScr, hScr = autopy.screen.size()

while True:
    # 1) Trovare i landmark della mano
    success, img = cap.read()
    img = cv2.flip(img, 1)
    img = detector.findHands(img)
    lmList, bbox = detector.findPosition(img)

    cv2.rectangle(img, (roiDim, roiDim), (wCam - roiDim, hCam - roiDim), (255, 255, 255),
                  2)  # roi (schermo in scala per non avere problemi nell'identificare la mano)

    # 2) Trovare la punta di indice e medio
    if len(lmList) != 0:
        x1, y1, = lmList[8][1:]  # indice
        x2, y2, = lmList[12][1:]  # medio

        # 3) Controllare quali dita sono sollevate
        fingers = detector.fingersUp()
        # print(fingers)

        # 4) MoveMode (indice su)
        if fingers[1]==1 and fingers[2]==0:

            # 5) Convertire le coordinate
            x3 = np.interp(x1, (roiDim, wCam-roiDim), (0, wScr))
            y3 = np.interp(y1, (roiDim, hCam-roiDim), (0, hScr))

            # 6) Smooth della coordinata
            cLocX = pLocX + (x3 - pLocX) / smoothening
            cLocY = pLocY + (y3 - pLocY) / smoothening

            # 7) Muovere il mouse
            autopy.mouse.move(cLocX, cLocY)
            cv2.circle(img, (x1, y1), 15, (219, 232, 233), cv2.FILLED)
            pLocX, pLocY = cLocX, cLocY

        # 8) ClickMode (indice e medio alzati)
        if fingers[1]==1 and fingers[2]==1:

            # 9) Trovare la distanza tra le dita
            length, img, _ = detector.findDistance(8, 12, img)
            #print(length)  # cercare una distanza adeguata

            # 10) Click se la distanza è breve
            if length < 30:
                cv2.circle(img, (x1, y1), 15, (175, 228, 131), 3)

                autopy.mouse.click()

        #if fingers[0] == 1:
        #    autopy.key.toggle('a', True)


    # 11) Frame rate
    cTime = time.time() # current time
    fps = 1/(cTime-pTime)
    pTime = cTime
    cv2.putText(img, str(int(fps)), (20, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)

    # 12) Visualizzazione
    cv2.imshow("Capture", img)
    cv2.waitKey(1)









