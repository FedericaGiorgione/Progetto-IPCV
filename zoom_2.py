import cv2
from cvzone.HandTrackingModule import HandDetector

def zoom(img, zoom_factor=2):
    return cv2.resize(img, None, fx=zoom_factor, fy=zoom_factor)




def main():
    cap = cv2.VideoCapture(0)
    cap.set(3, 1280)
    cap.set(4, 720)
    cx, cy = 640, 360

    n, m = 1, 1  # moltiplicatori per la dimensione delle slide
    wSmall, hSmall = int(213*n), int(120*m)  # dimensione slide

    detector = HandDetector(detectionCon=0.8)

    # serve per salvare la distanza inziale fra le dita prima dello zoom
    startDist = None
    scale = 1

    #conserviamo la posizione iniziale dell'indice se abbiamo zoom
    startIndexPositionX = None
    startIndexPositionY = None

    #servono a capire quanto ci spostiamo sull'immagine zoomata
    padX = 0
    padY = 0

    backgroundImg = cv2.imread("Slides/background.jpg")

    while True:
        success, img = cap.read()
        hands, img = detector.findHands(img)
        actualImage = cv2.imread("Slides/test2.jpg")
        #serve come base immutabile di schermata

        if len(hands) == 2:
            lmList1 = hands[0]["lmList"]
            lmList2 = hands[1]["lmList"]
            #print(detector.fingersUp(hands[0]), detector.fingersUp(hands[1]))
            if detector.fingersUp(hands[0]) == [0, 1, 0, 0, 0] and \
                detector.fingersUp(hands[1]) == [0, 1, 0, 0, 0]:
                print("Zoom Gesture")

                if startDist is None:
                    length, info, img = detector.findDistance(lmList1[8], lmList2[8], img)
                    startDist = length

                length, info, img = detector.findDistance(lmList1[8], lmList2[8], img)
                scale = float((length - startDist) / 60)
                if scale > 4:
                    scale = 4
                elif scale < 1:
                    scale = 1
                # conserviamo il punto centrale della distanza fra le dita
                cx, cy = info[4:]
                cx -= 200
                cy -= 100
                print("fattore di scala: ", scale)
                print(cx, cy)


            #gesture per movimento immagine se zoomata
            """"
            if detector.fingersUp(hands[0]) == [0, 1, 1, 0, 0] and \
                    detector.fingersUp(hands[1]) == [0, 0, 0, 0, 0] and scale > 1:
                print("gesture movimento zoom")
                print(lmList1[8])
                if startIndexPositionX is None:
                    startIndexPositionX, startIndexPositionY = lmList1[8][0], lmList1[8][1]
                else:
                    padX = lmList1[8][0] - startIndexPositionX
                    padY = lmList1[8][1] - startIndexPositionY
                    print(padX, padY)
            """

        else:
            startDist = None
            startIndexPositionX = None
            startIndexPositionY = None

            if len(hands) == 1:
                if detector.fingersUp(hands[0]) == [0, 1, 1, 0, 0]:
                    lmList1 = hands[0]["lmList"]
                    print("disegno abilitato")
                    cv2.line(img,lmList1[8][0], (720, 1280), (255, 0, 0), 2)




        actualImage = cv2.resize(actualImage, None, fx=scale, fy=scale)

        #zoom in alto a sinsitra
        #zoomedImg = actualImage[0:720, 0:1280]

        #zoom dal centro
        #haux, waux, _ = actualImage.shape
        #zoomedImg = actualImage[haux//2-360:haux//2+360, waux//2-640:waux//2+640]


        if cy - 360 < 0 and cx - 640 < 0:
            zoomedImg = actualImage[0:720, 0:1280]
        elif cy - 360 < 0 and cx + 640 > 1280:
            haux, waux, _ = actualImage.shape
            zoomedImg = actualImage[0:720, waux - 1280:waux]
        elif cy + 360 > 720 and cx - 640 < 0:
            haux, waux, _ = actualImage.shape
            zoomedImg = actualImage[haux-720:haux, 0:1280]
        elif cy + 360 > 720 and cx + 640 > 1280:
            haux, waux, _ = actualImage.shape
            zoomedImg = actualImage[haux - 720 :haux, waux - 1280:waux]
        elif  cy - 360 < 0:
            haux, waux, _ = actualImage.shape
            zoomedImg = actualImage[0:720, cx-640:cx+640]
        elif cy + 360 > 720:
            haux, waux, _ = actualImage.shape
            zoomedImg = actualImage[haux-720:haux, cx - 640:cx + 640]
        elif cx - 640 < 0:
            haux, waux, _ = actualImage.shape
            zoomedImg = actualImage[cy-360:cy+360, 0:1280]
        elif cx + 640 > 1280:
            haux, waux, _ = actualImage.shape
            zoomedImg = actualImage[cy-360:cy+360, waux - 1280:waux]
        else:
            zoomedImg = actualImage[cy-360:cy+360, cx-640:cx+640]


        #zoom con gesture alternativa
        #servono i controlli se si esce dallo schermo
        """"
        haux, waux, _ = actualImage.shape
        zoomedImg = actualImage[(haux+padY)//2-360:(haux+padY)//2+360, (waux+padX)//2-640:(waux+padX)//2+640]
        """

        # aggiungo la web cam in alto a destra
        webcamImg = cv2.resize(img, (wSmall, hSmall))
        h, w, _ = zoomedImg.shape
        zoomedImg[0:hSmall, w - wSmall:w] = webcamImg


        backgroundImg[0:, 0:] = zoomedImg

        #avvio la schermata con slide e webcam
        cv2.imshow("Presentation", backgroundImg)
        cv2.waitKey(1)



if __name__ == "__main__":
    main()
