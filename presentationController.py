# gestureThreshold modificabile
# salvare le note sulla singola pagina (rendere annotations una lista tripa, ovvero pagina->annotazione->punto)
# cambiare colore per disegnare

import os
import cv2
from cvzone.HandTrackingModule import HandDetector
import numpy as np

def main():
    # ---------VARIABILI---------

    width = 1280
    height = 720
    #folderPath = "Slides\\"
    folderPath = "temp\\"
    imgCount = 0

    n, m = 1, 1  # moltiplicatori per la dimensione delle slide
    wSmall, hSmall = int(213 * n), int(120 * m)  # dimensione slide

    detector = HandDetector(detectionCon=0.8, maxHands=2)
    rightHand = False
    leftHand = False

    gestureThreshold = 300  # soglia sopra la quale considerare un movimento come gesture
    buttonPressed = False
    buttonCounter = 0
    buttonDelay = 15  # delay di pressione del bottone (ovvero per quanti frame una gesture è valida prima che venga rilevata nuovamente)

    smoothening = 2  # alto -> cursore lento, basso -> cursore tremolante
    pLocX, pLocY = 0, 0
    cLocX, cLocY = 0, 0

    annotations = [[]]
    annotationCounter = 0  # indice di disegno (altrimenti viene disegnata una linea tra ogni disegno)
    annotationStart = False  # flag per far partire un nuovo disegno
    cColor = (0, 0, 255)  # colore di disegno corrente

    # ---------------------------

    cap = cv2.VideoCapture(0)  # seleziono la webcam
    cap.set(3, width)  # larghezza (id=3)
    cap.set(4, height)  # altezza (id=4)

    # prendo la lista delle immagini
    pathImgs = sorted(os.listdir(folderPath), key=len)  # ordino per linghezza così non ho problemi con le decine

    while True:
        # Importo le immagini
        success, img = cap.read()
        img = cv2.flip(img, 1)
        pathFullImgs = os.path.join(folderPath, pathImgs[imgCount])
        imgCurrent = cv2.imread(pathFullImgs)
        # imgCurrent = cv2.resize(imgCurrent, (width, height))  # resize a dimensione fissa

        # Rileva le mani
        hands, img = detector.findHands(img)
        cv2.line(img, (0, gestureThreshold), (width, gestureThreshold), (0, 255, 0), 5)
        cv2.rectangle(img, (width // 2, height - 200), (width-200, 200), (255, 255, 255), 2)  # ROI puntatore con mano destra
        cv2.rectangle(img, (200, height - 200), (width // 2, 200), (255, 255, 255), 2)  # ROI puntatore con mano sinistra

        rightHand = False
        leftHand = False

        if hands and buttonPressed == False:
            if hands[0]['type']=='Left':  # mano destra (flip)
                rightHand = True
                handR = hands[0]
                fingersR = detector.fingersUp(handR)
                cxR, cyR, = handR['center']  # centro della mano
                # print(fingers)
                lmListR = handR['lmList']
            else:
                leftHand = True
                handL = hands[0]
                fingersL = detector.fingersUp(handL)
                cxL, cyL, = handL['center']  # centro della mano
                # print(fingers)
                lmListL = handL['lmList']

            if len(hands) == 2:
                if hands[1]['type'] == 'Left':  # mano destra (flip)
                    rightHand = True
                    handR = hands[1]
                    fingersR = detector.fingersUp(handR)
                    cxR, cyR, = handR['center']  # centro della mano
                    # print(fingers)
                    lmListR = handR['lmList']
                else:
                    leftHand = True
                    handL = hands[1]
                    fingersL = detector.fingersUp(handL)
                    cxL, cyL, = handL['center']  # centro della mano
                    # print(fingers)
                    lmListL = handL['lmList']

            # ROI per il puntatore (metà destra schermo)
            if rightHand:
                xValR = int(np.interp(lmListR[8][0], [width // 2, imgCurrent.shape[1]-200], [0, width]))
                yValR = int(np.interp(lmListR[8][1], [200, height - 200], [0, height]))
                indexFingerR = xValR, yValR

            # ROI per il puntatore (metà sinistra schermo)
            if leftHand:
                xValL = int(np.interp(lmListL[8][0], [200, width // 2], [0, width]))
                yValL = int(np.interp(lmListL[8][1], [200, height - 200], [0, height]))
                indexFingerL = xValL, yValL

            # GESTURE A UNA MANO

            if rightHand:
                if cyR <= gestureThreshold:
                    annotationStart = False

                    # Gesture 1 - sinistra (pollice)
                    if fingersR == [1, 0, 0, 0, 0]:
                        annotationStart = False

                        # print("left")
                        if imgCount > 0:
                            buttonPressed = True
                            imgCount -= 1

                            annotations = [[]]
                            annotationCounter = 0

                    # Gesture 2 - destra (mignolo)
                    if fingersR == [0, 0, 0, 0, 1]:
                        annotationStart = False

                        # print("right")
                        if imgCount < len(pathImgs) - 1:
                            buttonPressed = True
                            imgCount += 1

                            annotations = [[]]
                            annotationCounter = 0
            if leftHand:
                if cyL <= gestureThreshold:
                    annotationStart = False

                    # Gesture 1 - sinistra (pollice)
                    if fingersL == [1, 0, 0, 0, 0]:
                        annotationStart = False

                        # print("left")
                        if imgCount > 0:
                            buttonPressed = True
                            imgCount -= 1

                            annotations = [[]]
                            annotationCounter = 0

                    # Gesture 2 - destra (mignolo)
                    if fingersL == [0, 0, 0, 0, 1]:
                        annotationStart = False

                        # print("right")
                        if imgCount < len(pathImgs) - 1:
                            buttonPressed = True
                            imgCount += 1

                            annotations = [[]]
                            annotationCounter = 0

            # Gesture 3 - Puntatore (indice)
            if rightHand and fingersR == [0, 1, 0, 0, 0]:
                cLocX = int(pLocX + (indexFingerR[0] - pLocX) / smoothening)
                cLocY = int(pLocY + (indexFingerR[1] - pLocY) / smoothening)
                indexFingerR = cLocX, cLocY

                cv2.circle(imgCurrent, indexFingerR, 8, (0, 0, 255), cv2.FILLED)
                annotationStart = False

                pLocX, pLocY = cLocX, cLocY
            elif leftHand and fingersL == [0, 1, 0, 0, 0]:
                cLocX = int(pLocX + (indexFingerL[0] - pLocX) / smoothening)
                cLocY = int(pLocY + (indexFingerL[1] - pLocY) / smoothening)
                indexFingerL = cLocX, cLocY

                cv2.circle(imgCurrent, indexFingerL, 8, (0, 0, 255), cv2.FILLED)
                annotationStart = False

                pLocX, pLocY = cLocX, cLocY

            # GESTURE A DUE MANI

            if rightHand and leftHand:
                # Gesture 4 - Disegno (indice e seconda mano chiusa)
                if fingersR == [0, 1, 0, 0, 0] and fingersL == [1, 1, 1, 1, 1]:
                    cLocX = int(pLocX + (indexFingerR[0] - pLocX) / smoothening)
                    cLocY = int(pLocY + (indexFingerR[1] - pLocY) / smoothening)
                    indexFingerR = cLocX, cLocY

                    if annotationStart is False:
                        annotationStart = True
                        annotationCounter += 1
                        annotations.append([])  # inizio un nuovo disegno

                    cv2.circle(imgCurrent, indexFingerR, 8, (0, 0, 255), cv2.FILLED)
                    annotations[annotationCounter].append(indexFingerR)

                    pLocX, pLocY = cLocX, cLocY

                elif fingersL == [0, 1, 0, 0, 0] and fingersR == [1, 1, 1, 1, 1]:
                    cLocX = int(pLocX + (indexFingerL[0] - pLocX) / smoothening)
                    cLocY = int(pLocY + (indexFingerL[1] - pLocY) / smoothening)
                    indexFingerL = cLocX, cLocY

                    if annotationStart is False:
                        annotationStart = True
                        annotationCounter += 1
                        annotations.append([])  # inizio un nuovo disegno

                    cv2.circle(imgCurrent, indexFingerL, 8, (0, 0, 255), cv2.FILLED)
                    annotations[annotationCounter].append(indexFingerL)

                    pLocX, pLocY = cLocX, cLocY
                else:
                    annotationStart = False

                # Gesture 5 - Cancella ultimo disegno (indice, medio e seconda mano chiusa)
                if fingersR == [1, 1, 0, 0, 0] and fingersL == [1, 1, 1, 1, 1]:
                    if annotations:
                        if annotationCounter >= 0:
                            annotations.pop(-1)
                            annotationCounter -= 1
                            buttonPressed = True

                if fingersL == [1, 1, 0, 0, 0] and fingersR == [1, 1, 1, 1, 1]:
                    if annotations:
                        if annotationCounter >= 0:
                            annotations.pop(-1)
                            annotationCounter -= 1
                            buttonPressed = True

        else:
            annotationStart = False

        if buttonPressed:
            buttonCounter += 1
            if buttonCounter > buttonDelay:
                buttonCounter = 0
                buttonPressed = False

        for i in range(len(annotations)):
            for j in range(len(annotations[i])):
                if j != 0:
                    print(len(annotationCounter), ' e ', annotations[i][j])
                    cv2.line(imgCurrent, annotations[i][j - 1], annotations[i][j], cColor,
                             5)  # disegna una linea tra ogni punto

        # 2) Aggiungo la webcam nella schermata delle slide
        imageSmall = cv2.resize(img, (wSmall, hSmall))
        h, w, _ = imgCurrent.shape
        imgCurrent[0:hSmall, w - wSmall:w] = imageSmall

        cv2.imshow("Image", img)
        cv2.imshow("Presentation", imgCurrent)

        key = cv2.waitKey(1)
        if key == ord('q'):
            break
        if (cv2.getWindowProperty('Presentation', 0) < 0):
            cv2.destroyAllWindows()
            break
        if (cv2.getWindowProperty('Image', 0) < 0):
            cv2.destroyAllWindows()
            break


if __name__ == "__main__":
    main()
