import os
import cv2
from cvzone.HandTrackingModule import HandDetector
import numpy as np
import os

import backgroundRemoval
import closureController
import numpy as np

tempDir = "temp/"
dictOfAnnotations = {}

def countNumberOfPages():
    count = 0
    for image in os.listdir(tempDir):
        count += 1
    return count



def main():
    # ---------VARIABILI---------

    width = 1280
    height = 720
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
    colorArray = [[]]


    #########################colori######################################
    black = (0, 0, 0)
    white = (255, 255, 255)
    red = (0, 0, 255)
    blue = (255, 0, 0)

    cColor = red  # colore di disegno corrente

    blackIcon = cv2.imread("image/black.png")
    blackIcon = cv2.resize(blackIcon, None, fx=0.2, fy=0.2)
    whiteIcon = cv2.imread("image/white.png")
    whiteIcon = cv2.resize(whiteIcon, None, fx=0.2, fy=0.2)
    redIcon = cv2.imread("image/red.png")
    redIcon = cv2.resize(redIcon, None, fx=0.2, fy=0.2)
    blueIcon = cv2.imread("image/blue.png")
    blueIcon = cv2.resize(blueIcon, None, fx=0.2, fy=0.2)

    tutorial = cv2.imread("image\\tutorial.png")

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

    cx, cy = None, None


    # ---------------------------

    cap = cv2.VideoCapture(0)  # seleziono la webcam
    cap.set(3, width)  # larghezza (id=3)
    cap.set(4, height)  # altezza (id=4)

    # prendo la lista delle immagini
    pathImgs = sorted(os.listdir(folderPath), key=len)  # ordino per linghezza così non ho problemi con le decine

    #variabile conteggio pagine
    auxCountPages = True
    numbersOfPages = 0

    #cinteggio numero note
    countNumber = 0
    auxCountNumber = True

    #booleani per visualizzazione camera e blur camera
    camera = True
    blur = False


    auxControlCamera = True
    auxControlBLur = True

    while True:

        #conto il numero totale di pagine presenti
        if auxCountPages:
            numbersOfPages = countNumberOfPages()
            auxCountPages = False


        # Importo le immagini
        success, img = cap.read()
        img = cv2.flip(img, 1)
        pathFullImgs = os.path.join(folderPath, pathImgs[imgCount])
        imgCurrent = cv2.imread(pathFullImgs)

        #conservo la camera pulita
        success2, clearImg = cap.read()

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
                if scale==1:
                    xValR = int(np.interp(lmListR[8][0], [width // 2, imgCurrent.shape[1]-200], [0, width]))
                    yValR = int(np.interp(lmListR[8][1], [200, height - 200], [0, height]))
                else:
                    xValR = int(np.interp(lmListR[8][0], [width // 2, imgCurrent.shape[1]-200], [int(padX/scale), int((padX-padXneg+width)/scale)]))
                    yValR = int(np.interp(lmListR[8][1], [200, height - 200], [int(padY/scale), int((padY-padYneg+height)/scale)]))
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
                                annotations = dictOfAnnotations[imgCount]['annotations']
                                colorArray = dictOfAnnotations[imgCount]['cColor']
                                annotationCounter = len(dictOfAnnotations[imgCount]['annotations'])-1
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
                                annotations = dictOfAnnotations[imgCount]['annotations']
                                colorArray = dictOfAnnotations[imgCount]['cColor']
                                annotationCounter = len(dictOfAnnotations[imgCount]['annotations']) - 1
                            else:
                                annotations = [[]]
                                colorArray = [[]]
                                annotationCounter = 0

                    # Gesture attivazione camera
                    if fingersR == [1, 0, 0, 0, 1]:
                        print("disattivo camera", camera)
                        if camera:
                            camera = False
                            buttonPressed = True
                        elif camera == False:
                            camera = True
                            buttonPressed = True

                    # Gesture attivazione blur
                    if len(hands) == 1:
                        if camera:
                            if fingersR == [0, 1, 1, 1, 1]:
                                if blur:
                                    blur = False
                                    buttonPressed = True
                                elif blur == False:
                                    blur = True
                                    buttonPressed = True
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
                            colorArray = [[]]
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
                            colorArray = [[]]
                            annotationCounter = 0

                    # Gesture attivazione camera
                    if fingersL == [1, 0, 0, 0, 1]:
                        print("disattivo camera", camera)
                        if camera:
                            camera = False
                            buttonPressed = True
                        elif camera == False:
                            camera = True
                            buttonPressed = True

                    # Gesture attivazione blur
                    if len(hands) == 1:
                        if camera:
                            if fingersL == [0, 1, 1, 1, 1]:
                                if blur:
                                    blur = False
                                    buttonPressed = True
                                elif blur == False:
                                    blur = True
                                    buttonPressed = True

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
                        annotationStart = True
                        annotationCounter += 1
                        annotations.append([])  # inizio un nuovo disegno
                        colorArray.append([])
                        dictOfAnnotations[imgCount] = []

                    cv2.circle(imgCurrent, indexFingerR, 8, cColor, cv2.FILLED)
                    annotations[annotationCounter].append(indexFingerR)
                    colorArray[annotationCounter].append(cColor)
                    dictOfAnnotations[imgCount] = {'annotations':annotations, 'cColor':colorArray}
                    print(dictOfAnnotations)

                    pLocX, pLocY = cLocX, cLocY

                elif fingersL == [0, 1, 0, 0, 0] and fingersR == [1, 1, 1, 1, 1]:
                    cLocX = int(pLocX + (indexFingerL[0] - pLocX) / smoothening)
                    cLocY = int(pLocY + (indexFingerL[1] - pLocY) / smoothening)
                    indexFingerL = cLocX, cLocY

                    if annotationStart is False:
                        annotationStart = True
                        annotationCounter += 1
                        annotations.append([])  # inizio un nuovo disegno
                        colorArray.append([])
                        dictOfAnnotations[imgCount] = annotations

                    cv2.circle(imgCurrent, indexFingerL, 8, cColor, cv2.FILLED)
                    annotations[annotationCounter].append(indexFingerL)
                    colorArray[annotationCounter].append(cColor)
                    dictOfAnnotations[imgCount] = {'annotations':annotations, 'cColor':colorArray}

                    pLocX, pLocY = cLocX, cLocY
                else:
                    annotationStart = False

                # Gesture 5 - Cancella ultimo disegno (indice, medio, pollice e seconda mano aperta)
                if fingersR == [1, 1, 1, 0, 0] and fingersL == [1, 1, 1, 1, 1]:
                    if annotations:
                        if annotationCounter >= 0:
                            annotations.pop(-1)
                            colorArray.pop(-1)
                            annotationCounter -= 1
                            dictOfAnnotations[imgCount] = {'annotations':annotations, 'cColor':colorArray}

                            buttonPressed = True

                if fingersL == [1, 1, 1, 0, 0] and fingersR == [1, 1, 1, 1, 1]:
                    if annotations:
                        if annotationCounter >= 0:
                            annotations.pop(-1)
                            colorArray.pop(-1)
                            annotationCounter -= 1
                            dictOfAnnotations[imgCount] = {'annotations':annotations, 'cColor':colorArray}
                            buttonPressed = True

                # Gesture 6 - Cancella tutti i disegni (entrmabi le amni aperte)
                if fingersL == [1, 1, 1, 1, 1] and fingersR == [1, 1, 1, 1, 1] and cyR<=gestureThreshold and cyR<=gestureThreshold:
                    if annotations:
                        if annotationCounter > 0:
                            annotations = [[]]
                            colorArray = [[]]
                            annotationCounter = 0
                            dictOfAnnotations[imgCount] = {'annotations':annotations, 'cColor':colorArray}
                            buttonPressed = True

                # Gesture 7 - Zoom
                if fingersR == [1, 1, 0, 0, 0] and fingersL == [1, 1, 0, 0, 0]:
                    if startDist is None:
                        length, info, img = detector.findDistance(lmListR[8], lmListL[8], img)
                        startDist = length

                    length, info, img = detector.findDistance(lmListR[8], lmListL[8], img)
                    scale = int((length - startDist) / 60)
                    if scale > 4:
                        scale = 4
                    elif scale < 1:
                        scale = 1

                # Gesture 8 - Cambio colore delle note
                if (fingersR == [1, 1, 1, 1, 1] and fingersL == [0, 1, 1, 1, 1]) or \
                        (fingersL == [1, 1, 1, 1, 1] and fingersR == [0, 1, 1, 1, 1]):
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

            # Gesture 9 - Movimento nell'immagine scalata
            if scale>1:
                if fingersR == [1, 1, 0, 0, 0]:
                    cx, cy, = lmListR[8][0], lmListR[8][1]
                elif fingersL == [1, 1, 0, 0, 0]:
                    cx, cy = lmListL[8][0], lmListL[8][1]
            else:
                cx, cy = None, None

        else:
            annotationStart = False

        if buttonPressed:
            buttonCounter += 1
            if buttonCounter > buttonDelay:
                buttonCounter = 0
                buttonPressed = False


        if len(dictOfAnnotations) != 0:
            if imgCount in dictOfAnnotations:
                note = dictOfAnnotations[imgCount]
                for i in range(len(note['annotations'])):
                    for j in range(len(note['annotations'][i])):
                        if j != 0:
                            # print(annotationCounter, ' e ', annotations[i][j])
                            cv2.line(imgCurrent, note['annotations'][i][j - 1], note['annotations'][i][j], note['cColor'][i][j],
                                     5)  # disegna una linea tra ogni punto

        #contiene l'immagine attuale, potrebbe essere scalato se applichiamo lo zoom
        imgCurrent = cv2.resize(imgCurrent, None, fx=scale, fy=scale)

        #prendiamo solo la porzione centrale dell'immagine quando zoomiamo
        haux, waux, _ = imgCurrent.shape
        zoomedImg = imgCurrent[haux//2-360:haux//2+360, waux//2-640:waux//2+640]


        #se l'immagine è scalata dobbiamo fare i controlli se prendiamo una porzione non della dimensione che ci serve
        if cx != None:
            if scale*cx > waux/4 and scale*cx < 3/4*waux and scale*cy > haux/4 and scale*cy < 3/4*haux:  # zona 9
                print('zona: ', 9)
                padY = int(cy * scale) - 360
                padX = int(cx * scale) - 640
                padYneg = int(cy * scale) - 360
                padXneg = int(cx * scale) - 640

                if padY < 0:
                    padY = 0
                else:
                    padYneg = 0

                if padX < 0:
                    padX = 0
                else:
                    padXneg = 0

                zoomedImg = imgCurrent[padY:int(cy * scale) + 360 + padYneg,
                                        padX:int(cx * scale) + 640 + padXneg]
            elif scale*cx < waux/4 and scale*cy < haux/4:  # zona 1
                print('zona: ', 1)
                padY = 0
                padX = 0
                zoomedImg = imgCurrent[0:720, 0:1280]
            elif scale*cx < waux/4 and scale*cy > haux*3/4:  # zona 7
                print('zona: ', 7)
                padY = haux-720
                padX = 0
                zoomedImg = imgCurrent[haux-720:haux, 0:1280]
            elif scale*cx < waux/4:  # zona 8
                print('zona: ', 8)
                padY = int(scale*cy)-360
                padX = 0
                zoomedImg = imgCurrent[int(scale*cy)-360:int(scale*cy)+360, 0:1280]
            elif scale*cx > 3/4*waux and scale*cy < haux/4:  # zona 3
                print('zona: ', 3)
                padY = 0
                padX = waux-1280
                zoomedImg = imgCurrent[0:720, waux-1280:waux]
            elif scale*cx > 3/4*waux and scale*cy > haux*3/4:  # zona 5
                print('zona: ', 5)
                padY = haux-720
                padX = waux-1280
                zoomedImg = imgCurrent[haux-720:haux, waux-1280:waux]
            elif scale*cx > 3/4*waux:  # zona 4
                print('zona: ', 4)
                padY = int(scale*cy)-360
                padX = waux-1280
                zoomedImg = imgCurrent[int(scale*cy)-360: int(scale*cy)+360, waux-1280: waux]
            elif scale*cy < haux/4:  # zona 2
                print('zona: ', 2)
                padY = 0
                padX = int(scale*cx)-640
                zoomedImg = imgCurrent[0:720, int(scale*cx)-640: int(scale*cx)+640]
            elif scale*cy > haux*3/4:  # zona 6
                padY = haux-720
                padX = int(scale * cx) - 640
                print('zona: ', 6)
                zoomedImg = imgCurrent[haux-720:haux, int(scale * cx) - 640: int(scale * cx) + 640]


        #ridimensiono l'immagine pulita per inserirla nelle slide
        clearImg = cv2.resize(clearImg, (wSmall, hSmall))

        #inserisco il blur se attivo
        if blur:
            clearImg = backgroundRemoval.blurBackground(clearImg, 11)


        #creazione interfaccia webcam con indicatori e info sui comandi
        imgSupport = np.concatenate((cv2.resize(img, (910, 512)), tutorial), axis=1)
        cv2.imshow("Gestures tutorial", imgSupport)

        #############creazione interfaccia utente##############


        backgroundImg = cv2.imread("image/background.jpg")
        checkedIcon = cv2.imread("image/checked.png")
        uncheckedIcon = cv2.imread("image/unchecked.png")


        #inserisco la cam in alto a destra
        if camera:
            backgroundImg[30:hSmall + 30, 30:wSmall + 30] = clearImg


        #ridimensiono l'immagine della slide per inserirla nel mio progetto
        resizedImg = cv2.resize(zoomedImg, None, fx=0.7, fy=0.7)
        auxY, auxX, _ = resizedImg.shape

        # inserimento immagine slide
        backgroundImg[100:auxY + 100, 300:auxX + 300] = resizedImg


        #inserimento switch camera
        if camera:
            checkY, checkX, _ = checkedIcon.shape
            backgroundImg[hSmall + 222: hSmall + checkY + 222, 60: 60+checkX] = checkedIcon
        else:
            checkY, checkX, _ = uncheckedIcon.shape
            backgroundImg[hSmall + 222: hSmall + checkY + 222, 60: 60 + checkX] = uncheckedIcon


        cv2.putText(backgroundImg, text='Camera', org=(100, hSmall + 242),
                    fontFace=cv2.FONT_HERSHEY_TRIPLEX, fontScale=0.8, color=(255, 255, 255), thickness=1)


        # inserimento switch blur
        if camera and blur:
            checkY, checkX, _ = checkedIcon.shape
            backgroundImg[hSmall + 267: hSmall + checkY + 267, 60: 60 + checkX] = checkedIcon
        else:
            checkY, checkX, _ = uncheckedIcon.shape
            backgroundImg[hSmall + 267: hSmall + checkY + 267, 60: 60 + checkX] = uncheckedIcon

        cv2.putText(backgroundImg, text='Blur Camera', org=(100, hSmall + 287),
                    fontFace=cv2.FONT_HERSHEY_TRIPLEX, fontScale=0.8, color=(255, 255, 255), thickness=1)



        # inserimento colori e bordo nel colore attivo
        grey = (128, 128, 128)
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
            backgroundImg[hSmall + 131: hSmall + 202, wSmall - 51: wSmall + 20] = activeColor
        else:
            backgroundImg[hSmall + 141: hSmall + 192, wSmall - 41: wSmall + 10] = whiteIcon


        #inserisco il numero della slide e il totale numero di slides presenti
        cv2.putText(backgroundImg, text=str(imgCount+1) + '/' + str(numbersOfPages), org=(1100, 80), fontFace=cv2.FONT_HERSHEY_TRIPLEX, fontScale=1, color=(255, 255, 255),thickness=2)



        #configurazione finestra a schermo intero (con barra sopra presente)
        cv2.namedWindow("Presentation", cv2.WND_PROP_FULLSCREEN)

        #visualizzazione schermata applicazione
        cv2.imshow("Presentation", backgroundImg)

        key = cv2.waitKey(1)

        #GESTIONE CHIUSURA FINESTRA
        if key == ord('q'):
            closureController.closingApp()
            #break
        elif cv2.getWindowProperty("Presentation", cv2.WND_PROP_VISIBLE) < 1:
            closureController.closingApp()
            #break

    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
