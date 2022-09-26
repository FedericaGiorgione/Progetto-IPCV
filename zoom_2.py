import cv2
from cvzone.HandTrackingModule import HandDetector
import autopy  # per muovere il mouse
import numpy as np

def zoom(img, zoom_factor=2):
    return cv2.resize(img, None, fx=zoom_factor, fy=zoom_factor)




def main():
    cap = cv2.VideoCapture(0)
    cap.set(3, 1280)
    cap.set(4, 720)
    cx, cy = None, None

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

    """
    wCam = 1280
    hCam = 720
    roiDim = 200

    wScr, hScr = autopy.screen.size()

    pLocX, pLocY = 0, 0
    cLocX, cLocY = 0, 0
    smoothening = 4  # alto -> cursore lento, basso -> cursore tremolante
    """

    backgroundImg = cv2.imread("Slides/background.jpg")

    while True:
        success, img = cap.read()
        hands, img = detector.findHands(img)
        actualImage = cv2.imread("Slides/test2.jpg")
        #serve come base immutabile di schermata

        #cv2.rectangle(img, (roiDim, roiDim), (wCam - roiDim, hCam - roiDim), (255, 255, 255), 2)

        if len(hands) == 2:

            cx = None
            cy = None

            lmList1 = hands[0]["lmList"]
            lmList2 = hands[1]["lmList"]
            #print(detector.fingersUp(hands[0]), detector.fingersUp(hands[1]))
            if detector.fingersUp(hands[0]) == [1, 1, 0, 0, 0] and \
                detector.fingersUp(hands[1]) == [1, 1, 0, 0, 0]:
                print("Zoom Gesture")
                if startDist is None:
                    length, info, img = detector.findDistance(lmList1[8], lmList2[8], img)
                    startDist = length

                length, info, img = detector.findDistance(lmList1[8], lmList2[8], img)
                scale = int((length - startDist) / 60)
                if scale > 4:
                    scale = 4
                elif scale < 1:
                    scale = 1
                # conserviamo il punto centrale della distanza fra gli indici
                #cx, cy = info[4:]
                print("fattore di scala: ", scale)
        elif len(hands) == 1:
            #startDist = None
            startIndexPositionX = None
            startIndexPositionY = None

            lmList = hands[0]["lmList"]

            """if len(hands) == 1:
                if detector.fingersUp(hands[0]) == [0, 1, 1, 0, 0]:
                    lmList1 = hands[0]["lmList"]
                    print("disegno abilitato")
                    cv2.line(img,lmList1[8][0], (720, 1280), (255, 0, 0), 2)
            """
            # gesture per movimento immagine se zoomata
            if detector.fingersUp(hands[0]) == [0, 1, 0, 0, 0] and scale > 1:
                cx, cy = lmList[8][0], lmList[8][1]
                print("coordinate indice:", cx, cy)
            else:
                cx = None
                cy = None

        #haux, waux, _ = actualImage.shape
        actualImage = cv2.resize(actualImage, None, fx=scale, fy=scale)

        #zoom in alto a sinsitra
        #zoomedImg = actualImage[0:720, 0:1280]

        #zoom dal centro
        haux, waux, _ = actualImage.shape
        zoomedImg = actualImage[haux//2-360:haux//2+360, waux//2-640:waux//2+640]

        print('haux= ', haux, 'waux= ',  waux)


        if cx != None:
            print('cx s= ', cx * scale, 'cy s= ', cy * scale)
            #530 > 640
            if scale*cx > waux/4 and scale*cx < 3/4*waux and scale*cy > haux/4 and scale*cy < 3/4*haux:
                print('ciao')
                zoomedImg = actualImage[int(cy * scale) - 360:int(cy * scale) + 360,
                            int(cx * scale) - 640:int(cx * scale) + 640]
            elif scale*cx < waux/4 and scale*cy < haux/4:
                zoomedImg = actualImage[0:720, 0:1280]
            elif scale*cx < waux/4 and scale*cy > haux*3/4:
                zoomedImg = actualImage[haux-720:haux, 0:1280]
            elif scale*cx < waux/4:
                zoomedImg = actualImage[int(scale*cy)-360:int(scale*cy)+360, 0:1280]
            elif scale*cx > 3/4*waux and scale*cy < haux/4:
                zoomedImg = actualImage[0:720, waux-1280:waux]
            elif scale*cx > 3/4*waux and scale*cy > haux*3/4:
                zoomedImg = actualImage[haux-720:haux, waux-1280:waux]
            elif scale*cx > 3/4*waux:
                zoomedImg = actualImage[int(scale*cy)-360: int(scale*cy)+360, waux-1280: waux]
            elif scale*cy < haux/4:
                zoomedImg = actualImage[0:720, int(scale*cx)-640: int(scale*cx)+640]
            elif scale*cy > haux*3/4:
                zoomedImg = actualImage[haux-720:haux, int(scale * cx) - 640: int(scale * cx) + 640]

        # if cx != None:
        #     if cy*scale - 360 < 0 and cx*scale - 640 < 0:
        #         print("1")
        #         print("gesture movimento zoom")
        #         print(int(lmList[8][0] * scale), int(lmList[8][1] * scale))
        #         zoomedImg = actualImage[0:720, 0:1280]
        #     elif cy*scale - 360 < 0 and cx*scale + 640 > 1280:
        #         print("2")
        #         print("gesture movimento zoom")
        #         print(int(lmList[8][0] * scale), int(lmList[8][1] * scale))
        #         haux, waux, _ = actualImage.shape
        #         zoomedImg = actualImage[0:720, waux - 1280:waux]
        #     elif cy*scale + 360 > 720 and cx*scale - 640 < 0:
        #         print("3")
        #         print("gesture movimento zoom")
        #         print(int(lmList[8][0] * scale), int(lmList[8][1] * scale))
        #         haux, waux, _ = actualImage.shape
        #         zoomedImg = actualImage[haux - 720:haux, 0:1280]
        #     elif cy*scale + 360 > 720 and cx*scale + 640 > 1280:
        #         print("4")
        #         print("gesture movimento zoom")
        #         print(int(lmList[8][0] * scale), int(lmList[8][1] * scale))
        #         haux, waux, _ = actualImage.shape
        #         zoomedImg = actualImage[haux - 720:haux, waux - 1280:waux]
        #     elif cy*scale - 360 < 0:
        #         print("5")
        #         print("gesture movimento zoom")
        #         print(int(lmList[8][0] * scale), int(lmList[8][1] * scale))
        #         haux, waux, _ = actualImage.shape
        #         zoomedImg = actualImage[0:720, int(cx * scale) - 640:int(cx * scale) + 640]
        #     elif cy*scale + 360 > 720:
        #         print("6")
        #         print("gesture movimento zoom")
        #         print(int(lmList[8][0] * scale), int(lmList[8][1] * scale))
        #         haux, waux, _ = actualImage.shape
        #         zoomedImg = actualImage[haux - 720:haux, int(cx * scale) - 640:int(cx * scale) + 640]
        #     elif cx*scale - 640 < 0:
        #         print("7")
        #         print("gesture movimento zoom")
        #         print(int(lmList[8][0] * scale), int(lmList[8][1] * scale))
        #         haux, waux, _ = actualImage.shape
        #         zoomedImg = actualImage[int(cy * scale) - 360:int(cy * scale) + 360, 0:1280]
        #     elif cx*scale + 640 > 1280:
        #         print("8")
        #         print("gesture movimento zoom")
        #         print(int(lmList[8][0] * scale), int(lmList[8][1] * scale))
        #         haux, waux, _ = actualImage.shape
        #         zoomedImg = actualImage[int(cy * scale) - 360:int(cy * scale) + 360, waux - 1280:waux]
        #     else:
        #         print("9")
        #         print("gesture movimento zoom")
        #         print(int(lmList[8][0] * scale), int(lmList[8][1] * scale))
        #         zoomedImg = actualImage[int(cx * scale) - 360:int(cx * scale) + 360, int(cy * scale) - 640:int(cy * scale) + 640]


        #zoom con movimento che segue il centro fra gli indici
        """
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
        """

        #zoom con gesture alternativa
        #servono i controlli se si esce dallo schermo
        """haux, waux, _ = actualImage.shape
        zoomedImg = actualImage[(haux+padY)//2-360:(haux+padY)//2+360, (waux+padX)//2-640:(waux+padX)//2+640]
        """

        # aggiungo la web cam in alto a destra
        webcamImg = cv2.resize(img, (wSmall, hSmall))
        h, w, _ = zoomedImg.shape
        zoomedImg[0:hSmall, w - wSmall:w] = webcamImg


        backgroundImg[0:, 0:] = zoomedImg

        #avvio la schermata con slide e webcam
        cv2.imshow("Presentation", backgroundImg)
        cv2.imshow("Webcam Debug", img)
        cv2.waitKey(1)



if __name__ == "__main__":
    main()
