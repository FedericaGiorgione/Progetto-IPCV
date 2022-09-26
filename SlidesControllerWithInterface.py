# gestureThreshold modificabile
# salvare le note sulla singola pagina (rendere annotations una lista tripa, ovvero pagina->annotazione->punto)
# cambiare colore per disegnare

import os
import cv2
from cvzone.HandTrackingModule import HandDetector
import numpy as np
import os
import closureController

dictOfAnnotations = {}

def main():
    # ---------VARIABILI---------

    width = 1280
    height = 720
    folderPath = "Slides\\"
    #folderPath = "temp\\"
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


    #########################colori######################################
    black = (0, 0, 0)
    white = (255, 255, 255)
    red = (0, 0, 255)
    blue = (128, 0, 128)
    yellow = (255, 255, 0)

    cColor = red  # colore di disegno corrente

    blackIcon = cv2.imread("image/black.png")
    blackIcon = cv2.resize(blackIcon, None, fx=0.2, fy=0.2)
    whiteIcon = cv2.imread("image/white.png")
    whiteIcon = cv2.resize(whiteIcon, None, fx=0.2, fy=0.2)
    redIcon = cv2.imread("image/red.png")
    redIcon = cv2.resize(redIcon, None, fx=0.2, fy=0.2)
    blueIcon = cv2.imread("image/blue.png")
    blueIcon = cv2.resize(blueIcon, None, fx=0.2, fy=0.2)
    #yellowIcon = cv2.imread("image/yellow.png")
    #yellowIcon = cv2.resize(yellowIcon, None, fx=0.2, fy=0.2)

    changeColor = True
    ###############################################################################


    n, m = 1, 1  # moltiplicatori per la dimensione delle slide
    # serve per salvare la distanza inziale fra le dita prima dello zoom
    startDist = None
    scale = 1

    #conserviamo la posizione iniziale dell'indice se abbiamo zoom
    startIndexPositionX = None
    startIndexPositionY = None

    #servono a capire quanto ci spostiamo sull'immagine zoomata
    padX = 0
    padY = 0


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
                            scale = 1
                            imgCount -= 1
                            if imgCount in dictOfAnnotations:
                                annotations = dictOfAnnotations[imgCount]
                                annotationCounter = len(dictOfAnnotations[imgCount])-1
                            else:
                                annotations = [[]]
                                annotationCounter = 0

                    # Gesture 2 - destra (mignolo)
                    if fingersR == [0, 0, 0, 0, 1]:
                        annotationStart = False

                        # print("right")
                        if imgCount < len(pathImgs) - 1:
                            buttonPressed = True
                            scale = 1
                            imgCount += 1

                            if imgCount in dictOfAnnotations:
                                annotations = dictOfAnnotations[imgCount]
                                annotationCounter = len(dictOfAnnotations[imgCount]) - 1
                            else:
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
                            scale = 1
                            imgCount -= 1

                            annotations = [[]]
                            annotationCounter = 0

                    # Gesture 2 - destra (mignolo)
                    if fingersL == [0, 0, 0, 0, 1]:
                        annotationStart = False

                        # print("right")
                        if imgCount < len(pathImgs) - 1:
                            buttonPressed = True
                            scale = 1
                            imgCount += 1
                            annotations = [[]]
                            annotationCounter = 0

            # Gesture 3 - Puntatore (indice)
            if rightHand and fingersR == [0, 1, 0, 0, 0]:
                cLocX = int(pLocX + (indexFingerR[0] - pLocX) / smoothening)
                cLocY = int(pLocY + (indexFingerR[1] - pLocY) / smoothening)
                indexFingerR = cLocX, cLocY

                cv2.circle(imgCurrent, indexFingerR, 8, cColor, cv2.FILLED)
                #annotationStart = False

                pLocX, pLocY = cLocX, cLocY
            elif leftHand and fingersL == [0, 1, 0, 0, 0]:
                cLocX = int(pLocX + (indexFingerL[0] - pLocX) / smoothening)
                cLocY = int(pLocY + (indexFingerL[1] - pLocY) / smoothening)
                indexFingerL = cLocX, cLocY

                cv2.circle(imgCurrent, indexFingerL, 8, cColor, cv2.FILLED)
                #annotationStart = False

                pLocX, pLocY = cLocX, cLocY

            # GESTURE A DUE MANI

            if rightHand and leftHand:
                # Gesture 4 - Disegno (indice e seconda mano aperta)
                if fingersR == [0, 1, 0, 0, 0] and fingersL == [1, 1, 1, 1, 1]:
                    cLocX = int(pLocX + (indexFingerR[0] - pLocX) / smoothening)
                    cLocY = int(pLocY + (indexFingerR[1] - pLocY) / smoothening)
                    indexFingerR = cLocX, cLocY

                    if annotationStart is False:
                        print('siamo dentro')
                        annotationStart = True
                        annotationCounter += 1
                        annotations.append([])  # inizio un nuovo disegno
                        dictOfAnnotations[imgCount] = []

                    cv2.circle(imgCurrent, indexFingerR, 8, (0, 0, 255), cv2.FILLED)
                    annotations[annotationCounter].append(indexFingerR)
                    dictOfAnnotations[imgCount] = annotations


                    pLocX, pLocY = cLocX, cLocY

                elif fingersL == [0, 1, 0, 0, 0] and fingersR == [1, 1, 1, 1, 1]:
                    cLocX = int(pLocX + (indexFingerL[0] - pLocX) / smoothening)
                    cLocY = int(pLocY + (indexFingerL[1] - pLocY) / smoothening)
                    indexFingerL = cLocX, cLocY

                    if annotationStart is False:
                        annotationStart = True
                        annotationCounter += 1
                        annotations.append([])  # inizio un nuovo disegno
                        dictOfAnnotations[imgCount] = annotations

                    cv2.circle(imgCurrent, indexFingerL, 8, (0, 0, 255), cv2.FILLED)
                    annotations[annotationCounter].append(indexFingerL)
                    dictOfAnnotations[imgCount] = annotations

                    pLocX, pLocY = cLocX, cLocY
                else:
                    annotationStart = False

                # Gesture 5 - Cancella ultimo disegno (indice, medio, pollice e seconda mano aperta)
                if fingersR == [1, 1, 1, 0, 0] and fingersL == [1, 1, 1, 1, 1]:
                    if annotations:
                        if annotationCounter >= 0:
                            annotations.pop(-1)
                            annotationCounter -= 1
                            dictOfAnnotations[imgCount] = annotations
                            print(dictOfAnnotations)
                            buttonPressed = True

                if fingersL == [1, 1, 1, 0, 0] and fingersR == [1, 1, 1, 1, 1]:
                    if annotations:
                        if annotationCounter >= 0:
                            annotations.pop(-1)
                            annotationCounter -= 1
                            dictOfAnnotations[imgCount] = annotations
                            print(dictOfAnnotations)
                            buttonPressed = True

                # Gesture 6 - Cancella tutti i disegni (entrmabi le amni aperte)
                if fingersL == [1, 1, 1, 1, 1] and fingersR == [1, 1, 1, 1, 1]:
                    if annotations:
                        if annotationCounter > 0:
                            annotations = [[]]
                            annotationCounter = 0
                            dictOfAnnotations[imgCount] = annotations
                            print(dictOfAnnotations)
                            buttonPressed = True

                # Gesture 7 - Zoom
                if fingersR == [1, 1, 0, 0, 0] and fingersL == [1, 1, 0, 0, 0]:
                    if startDist is None:
                        length, info, img = detector.findDistance(lmListR[8], lmListL[8], img)
                        startDist = length

                    length, info, img = detector.findDistance(lmListR[8], lmListL[8], img)
                    scale = float((length - startDist) / 60)
                    if scale > 4:
                        scale = 4
                    elif scale < 1:
                        scale = 1
                    # conserviamo il punto centrale della distanza fra gli indici
                    # cx, cy = info[4:]
                    print("fattore di scala: ", scale)

                ####################gesture per cambio colore#######################################
                if fingersR == [1, 1, 1, 0, 0] and fingersL == [1, 1, 1, 0, 0]:
                    print("cambio colore")
                    if changeColor:
                        changeColor = False
                        if cColor == red:
                            cColor = blue
                        elif cColor == blue:
                            cColor = black
                        elif cColor == black:
                            cColor = white
                        elif cColor == white:
                            cColor = red
                else:
                    changeColor = True

                ######################################################################################

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
                    #print(annotationCounter, ' e ', annotations[i][j])
                    cv2.line(imgCurrent, annotations[i][j - 1], annotations[i][j], cColor,
                             5)  # disegna una linea tra ogni punto


        """
        for i in range(len(annotations)):
            for j in range(len(annotations[i])):
                if j != 0:
                    #print(annotationCounter, ' e ', annotations[i][j])
                    cv2.line(imgCurrent, annotations[i][j - 1], annotations[i][j], cColor,
                             5)  # disegna una linea tra ogni punto
        """

        if len(dictOfAnnotations) != 0:
            if imgCount in dictOfAnnotations:
                note = dictOfAnnotations[imgCount]
                for i in range(len(note)):
                    for j in range(len(note[i])):
                        if j != 0:
                            # print(annotationCounter, ' e ', annotations[i][j])
                            cv2.line(imgCurrent, note[i][j - 1], note[i][j], cColor,
                                     5)  # disegna una linea tra ogni punto

        imgCurrent = cv2.resize(imgCurrent, None, fx=scale, fy=scale)

        # zoom dal centro
        haux, waux, _ = imgCurrent.shape
        zoomedImg = imgCurrent[haux // 2 - 360:haux // 2 + 360, waux // 2 - 640:waux // 2 + 640]

#######################creazione immagine di sfondo e resize delle slide#################################
        auxZoomedImg = zoomedImg #1280x720
        auxImgCurrent = cv2.resize(auxZoomedImg, None, fx=0.7, fy=0.7) #640x360


###################################################################################

        # 2) Aggiungo la webcam nella schermata delle slide
        imageSmall = cv2.resize(img, (wSmall, hSmall))
        #h, w, _ = imgCurrent.shape
        h, w, _ = zoomedImg.shape

        zoomedImg[0:hSmall, w - wSmall:w] = imageSmall

        imgCurrent = cv2.resize(zoomedImg, None, fx=1, fy=1)
        imgCurrent[0:, 0:] = zoomedImg

        auxY, auxX, _ = auxImgCurrent.shape
        imgCurrent[100:auxY + 100, 300:auxX + 300] = auxImgCurrent

        cv2.imshow("Image", img)
        cv2.imshow("Presentation", imgCurrent)

        key = cv2.waitKey(1)


###########################INTERFACCIA A TUTTO SCHERMO###############################################
        backgroundImg = cv2.imread("image/background.jpg")

        #imgResized = cv2.resize(auxZoomedImg, None, fx=0.2, fy=0.2)

        #inserimento camera
        backgroundImg[30:hSmall+30, 30:wSmall+30] = imageSmall
        auxY, auxX, _ = auxImgCurrent.shape
        print(auxX, auxY)

        #inserimento immagine slide
        backgroundImg[100:auxY + 100, 300:auxX + 300] = auxImgCurrent




        #inserimento colori e bordo nel colore attivo
        grey = (128,128,128)
        if cColor == red:
            # inserisco il bordo nel colore attivo
            activeColor = cv2.copyMakeBorder(redIcon, 10, 10, 10, 10, cv2.BORDER_CONSTANT, value=grey)
            backgroundImg[hSmall + 50: hSmall + 121, 50: 121] = activeColor
        else:
            backgroundImg[hSmall + 60: hSmall + 111, 60: 111] = redIcon

        if cColor == blue:
            # inserisco il bordo nel colore attivo
            activeColor = cv2.copyMakeBorder(blueIcon, 10, 10, 10, 10, cv2.BORDER_CONSTANT, value=grey)
            backgroundImg[hSmall + 50: hSmall + 121, wSmall - 51: wSmall + 20] = activeColor
        else:
            backgroundImg[hSmall + 60: hSmall + 111, wSmall - 41: wSmall + 10] = blueIcon

        if cColor == black:
            # inserisco il bordo nel colore attivo
            activeColor = cv2.copyMakeBorder(blackIcon, 10, 10, 10, 10, cv2.BORDER_CONSTANT, value=grey)
            backgroundImg[hSmall + 131: hSmall + 202, 50: 121] = activeColor
        else:
            backgroundImg[hSmall + 141: hSmall + 192, 60: 111] = blackIcon

        if cColor == white:
            # inserisco il bordo nel colore attivo
            activeColor = cv2.copyMakeBorder(whiteIcon, 10, 10, 10, 10, cv2.BORDER_CONSTANT, value=grey)
            backgroundImg[hSmall + 131: hSmall + 202, wSmall - 51: wSmall +20] = activeColor
        else:
            backgroundImg[hSmall + 141: hSmall + 192, wSmall - 41: wSmall + 10] = whiteIcon



        cv2.namedWindow("window", cv2.WND_PROP_FULLSCREEN)
        #cv2.setWindowProperty("window", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
        cv2.imshow("window", backgroundImg)



########################################################################################################

        #GESTIONE CHIUSURA FINESTRA
        if key == ord('q'):
            closureController.closingApp()
            #break
        elif cv2.getWindowProperty("Presentation", cv2.WND_PROP_VISIBLE) < 1:
            closureController.closingApp()
            #break
        elif cv2.getWindowProperty("Image", cv2.WND_PROP_VISIBLE) < 1:
            closureController.closingApp()
            #break



    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
