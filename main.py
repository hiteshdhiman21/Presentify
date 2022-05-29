from cvzone.HandTrackingModule import HandDetector
import cv2
import os
import numpy as np

detectorHand = HandDetector(detectionCon=0.8, maxHands=1)

# Setting Parameters
width, height = 1280, 720
gestureThreshold = 300
folderPath = "Presentation"

# Setup camera
cap = cv2.VideoCapture(0)
cap.set(3, width)
cap.set(4, height)


imgList = []
delay = 30
isButtonPressed = False
drawMode = False
imgNumber = 0
counter = 0
delayCounter = 0
annotations = [[]]
annotationNumber = -1
annotationStart = False
hs, ws = int(120 * 1), int(213 * 1)  

# Getting the presentation images
pathImages = sorted(os.listdir(folderPath), key=len)
print(pathImages)

while True:
    # Get image frame one by one
    success, img = cap.read()
    img = cv2.flip(img, 1)
    pathFullImage = os.path.join(folderPath, pathImages[imgNumber])
    currentImg = cv2.imread(pathFullImage)

    hands, img = detectorHand.findHands(img) 
  
    cv2.line(img, (0, gestureThreshold), (width, gestureThreshold), (0, 255, 0), 10)

    if hands and isButtonPressed is False:  

        hand = hands[0]
        cx, cy = hand["center"]
        lmList = hand["lmList"]  
        fingers = detectorHand.fingersUp(hand)  

        xVal = int(np.interp(lmList[8][0], [width // 2, width], [0, width]))
        yVal = int(np.interp(lmList[8][1], [150, height-150], [0, height]))
        indexFinger = xVal, yVal

        if cy <= gestureThreshold:  
            if fingers == [1, 0, 0, 0, 0]:
                print("Left")
                isButtonPressed = True
                if imgNumber > 0:
                    imgNumber -= 1
                    annotations = [[]]
                    annotationNumber = -1
                    annotationStart = False
            if fingers == [0, 0, 0, 0, 1]:
                print("Right")
                isButtonPressed = True
                if imgNumber < len(pathImages) - 1:
                    imgNumber += 1
                    annotations = [[]]
                    annotationNumber = -1
                    annotationStart = False

        if fingers == [0, 1, 1, 0, 0]:
            cv2.circle(currentImg, indexFinger, 12, (0, 0, 255), cv2.FILLED)

        if fingers == [0, 1, 0, 0, 0]:
            if annotationStart is False:
                annotationStart = True
                annotationNumber += 1
                annotations.append([])
            print(annotationNumber)
            annotations[annotationNumber].append(indexFinger)
            cv2.circle(currentImg, indexFinger, 12, (0, 0, 255), cv2.FILLED)

        else:
            annotationStart = False

        if fingers == [0, 1, 1, 1, 0]:
            if annotations:
                annotations.pop(-1)
                annotationNumber -= 1
                isButtonPressed = True

    else:
        annotationStart = False

    if isButtonPressed:
        counter += 1
        if counter > delay:
            counter = 0
            isButtonPressed = False

    for i, annotation in enumerate(annotations):
        for j in range(len(annotation)):
            if j != 0:
                cv2.line(currentImg, annotation[j - 1], annotation[j], (0, 0, 200), 12)

    smallImg = cv2.resize(img, (ws, hs))
    h, w, _ = currentImg.shape
    currentImg[0:hs, w - ws: w] = smallImg

    cv2.imshow("Slides", currentImg)
    cv2.imshow("Image", img)

    key = cv2.waitKey(1)
    if key == ord('q'):
        break