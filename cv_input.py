import asyncio
import websockets
import cv2
import mediapipe as mp
import time

async def handler(websocket, path):
    print("open socket")
    mpHands = mp.solutions.hands
    hands = mpHands.Hands(static_image_mode=False,
                        max_num_hands=1,
                        min_detection_confidence=0.5,
                        min_tracking_confidence=0.5)
    mpDraw = mp.solutions.drawing_utils
    cap = cv2.VideoCapture(0)
    coordRes = pow(2,10) 
    # use VideoCapture(0) to use local (built in) webcam
    # use VideoCapture(1) to use a USB webcam
    cap = cv2.VideoCapture(0) 
    coordRes = pow(2,10)
    message = ""


    while True and websocket.open:
        success, img = cap.read()
        img = cv2.flip(img, 1)
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = hands.process(imgRGB)

        if results.multi_hand_landmarks:
            handLm = results.multi_hand_landmarks[0].landmark
            lm = handLm[8]
            h, w, c = img.shape
            cx, cy = int(lm.x *coordRes), int(lm.y *coordRes)
            # to get the purple line that tracks the index finger, uncomment the following two lines
            # cv2.circle(img, (cx,cy), 3, (255,0,255), cv2.FILLED)
            # cv2.line(img, (0,0), (cx,cy), (255,0,255), 3)
            # print(cx, cy)
            # if (msg != ""):
            #     message = msg + str(cx)+' '+str(cy)
            # else :
            message = str(cx) + " " + str(cy)
            #print(message)

        await websocket.send(message)



async def main():
    async with websockets.serve(handler, "localhost", 8765):
        await asyncio.Future()  # run forever
       
if __name__ == "__main__":
    asyncio.run(main())