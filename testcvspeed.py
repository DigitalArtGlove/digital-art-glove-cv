import cv2
import mediapipe as mp
import time

cap = cv2.VideoCapture(0) # use VideoCapture(0) to use local (built in) webcam
# cap = cv2.VideoCapture(1) # use VideoCapture(1) to use a USB webcam

mpHands = mp.solutions.hands
hands = mpHands.Hands(static_image_mode=False,
                      max_num_hands=1,
                      min_detection_confidence=0.5,
                      min_tracking_confidence=0.5)
mpDraw = mp.solutions.drawing_utils

pTime = 0
cTime = 0

starttime = time.time_ns()
count = 0
while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)
    # print(results.multi_hand_landmarks)

    if results.multi_hand_landmarks:
        handLm = results.multi_hand_landmarks[0].landmark
        lm = handLm[8]
        h, w, c = img.shape
        cx, cy = int(lm.x *w), int(lm.y*h)
        # cv2.circle(img, (cx,cy), 3, (255,0,255), cv2.FILLED)
        # cv2.line(img, (0,0), (cx,cy), (255,0,255), 3)

    # cv2.putText(img,str(int(fps)), (10,70), cv2.FONT_HERSHEY_PLAIN, 3, (255,0,255), 3)

    # cv2.imshow("Image", img)
    # cv2.waitKey(1)

    count += 1
    if (count >= 100):
        endtime = time.time_ns()
        timelapsed = (endtime - starttime)/1000000000
        print("Samples per second: " + str(100.0/timelapsed))
        break