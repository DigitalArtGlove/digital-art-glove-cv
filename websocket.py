import asyncio
import websockets
import cv2
import mediapipe as mp
import time
# import serial

# ser = serial.Serial(
#     port="/dev/cu.ESP32", baudrate=115200, bytesize=8, timeout=1, stopbits=serial.STOPBITS_ONE
# )
# ser.setDTR(False)
# ser.setRTS(False)

# if not ser.is_open:
#     ser.open()


async def handler(websocket, path):
    print("open socket")
    mpHands = mp.solutions.hands
    hands = mpHands.Hands(static_image_mode=False,
                        max_num_hands=1,
                        min_detection_confidence=0.5,
                        min_tracking_confidence=0.5)
    mpDraw = mp.solutions.drawing_utils
    cap = cv2.VideoCapture(0) # use VideoCapture(0) to use local (built in) webcam
    # cap = cv2.VideoCapture(1) # use VideoCapture(1) to use a USB webcam
    # while True and websocket.open and ser.open:
    starttime = time.time_ns()
    count = 0
    while True and websocket.open:
        success, img = cap.read()
        img = cv2.flip(img, 1)
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = hands.process(imgRGB)
        message = ""

        # msg = ser.readline().decode()
        # if (msg != ""):
        #     message = msg

        if results.multi_hand_landmarks:
            handLm = results.multi_hand_landmarks[0].landmark
            lm = handLm[8]
            h, w, c = img.shape
            cx, cy = int(lm.x*w), int(lm.y*h)
                        # to get the purple line that tracks the index finger, uncomment the following two lines
                        # cv2.circle(img, (cx,cy), 3, (255,0,255), cv2.FILLED)
                        # cv2.line(img, (0,0), (cx,cy), (255,0,255), 3)
                        # print(cx, cy)
                        # if (msg != ""):
                        #     message = msg + str(cx)+' '+str(cy)
                        # else :
            message = '0'+' '+'0'+' '+'0'+' '+'0'+' '+'0'+' '+'0'+' '+'0'+' '+'0'+' '+'0'+' '+'0'+' '+str(cx)+' '+str(cy)
            #print(message)
            break
        
        await websocket.send(message)
        
        count += 1
        if (count >= 100):
            endtime = time.time_ns()
            timelapsed = (endtime - starttime)/1000000000
            print("Samples per second: " + str(100.0/timelapsed))
            break


async def main():
    async with websockets.serve(handler, "localhost", 8765):
        await asyncio.Future()  # run forever
       
if __name__ == "__main__":
    asyncio.run(main())
