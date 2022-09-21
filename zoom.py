import cv2
from cvzone.HandTrackingModule import HandDetector

cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)


detector = HandDetector(detectionCon=0.8)

#serve per salvare la distanza inziale fra le dita prima dello zoom
startDist = None

scale = 0
cx, cy = 500, 500

while True:
    #creiamo l'interfaccia con l'immagine e il video
    success, img = cap.read()
    hands, img = detector.findHands(img)
    img1 = cv2.imread("Slides/sqrpop.jpg")

    #se abbiamo due mani a schermo fai qualcosa
    if len(hands)==2:
        #i vettori qui sotto descritti ci verificano quali dita della nostra mano sono aperti
        #print(detector.fingersUp(hands[0]), detector.fingersUp(hands[1]))
        # controlliamo che in entrmabe le mani solo pollice ed indice siano aperte
        if detector.fingersUp(hands[0])==[1,1,0,0,0] and\
                detector.fingersUp(hands[1])==[1,1,0,0,0]:
            #print("Zoom Gesture")
            #i vettori sotto contengono tutti i punti di controllo delle dita  cone le loro coordinate (x,y,z)
            lmList1 = hands[0]["lmList"]
            lmList2 = hands[1]["lmList"]
            #il punto 8 delle liste è la punta dell'indice
            #dobbiamo valutare la distanza fra i due indici per fare lo zoom
            #se è la prima volta vi settiamo la distanza inziale nella variabile startDist
            if startDist is None:
                length, info, img = detector.findDistance(lmList1[8], lmList2[8], img)
                # se volessimo mettere l'immagine al cetro della mano e non delle dita, trovaiamo la distanza fra le mani
                #length, info, img = detector.findDistance(hands[0]["center"], hands[1]["center"], img)
                #print(length)
                startDist = length

            length, info, img = detector.findDistance(lmList1[8], lmList2[8], img)
            #se volessimo mettere l'immagine al cetro della mano e non delle dita, trovaiamo la distanza fra le mani
            #length, info, img = detector.findDistance(hands[0]["center"], hands[1]["center"], img)
            scale = int((length -startDist)//2)
            #conserviamo il punto centrale della distanza fra le dita
            cx, cy = info[4:]
            print(scale)
    else:
        #serve per risettstr a None la distanza iniziale quando togliamo le mani dallo schermo
        startDist = None

    try:
        h1, w1, _= img1.shape
        newH, newW = ((h1+scale)//2)*2, ((w1+scale)//2)*2
        img1 = cv2.resize(img1, (newW, newH))

        #inserisco l'immagine dentro il video
        #img[10:260, 10:260] = img1
        img[cy-newH//2:cy+newH//2, cx-newW//2:cx+ newW//2] = img1
    except:
        pass



    #mostro il pannello con video e immagine
    cv2.imshow("Image", img)
    cv2.waitKey(1)