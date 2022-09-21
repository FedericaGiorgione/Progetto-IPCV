import cv2
from cvzone.HandTrackingModule import HandDetector

def zoom(img, zoom_factor=2):
    return cv2.resize(img, None, fx=zoom_factor, fy=zoom_factor)




def main():
    cap = cv2.VideoCapture(0)
    cap.set(3, 1280)
    cap.set(4, 720)

    n, m = 1, 1  # moltiplicatori per la dimensione delle slide
    wSmall, hSmall = int(213*n), int(120*m)  # dimensione slide

    detector = HandDetector(detectionCon=0.8)

    startDist = None
    scale = 1

    backgroundImg = cv2.imread("Slides/background.jpg")

    while True:
        success, img = cap.read()
        hands, img = detector.findHands(img)
        actualImage = cv2.imread("Slides/test.jpg")
        #serve come base immutabile di schermata


        if len(hands) == 2:
            #print(detector.fingersUp(hands[0]), detector.fingersUp(hands[1]))
            if detector.fingersUp(hands[0]) == [1, 1, 0, 0, 0] and \
                detector.fingersUp(hands[1]) == [1, 1, 0, 0, 0]:
                print("Zoom Gesture")
                lmList1 = hands[0]["lmList"]
                lmList2 = hands[1]["lmList"]
                if startDist is None:
                    length, info, img = detector.findDistance(lmList1[8], lmList2[8], img)
                    startDist = length

                length, info, img = detector.findDistance(lmList1[8], lmList2[8], img)
                scale = float((length - startDist) / 60)
                if scale > 4:
                    scale = 4
                elif scale < 1:
                    scale = 1
                print(scale)
        else:
            startDist = None

        actualImage = cv2.resize(actualImage, None, fx=scale, fy=scale)

        zoomedImg = actualImage[0:720, 0:1280]

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
