import asyncio
import websockets
import time
import cv2
import mediapipe as mp
import functools

import serial

# ser = serial.Serial(
#     port="/dev/cu.ESP32test", baudrate=115200, bytesize=8, timeout=1, stopbits=serial.STOPBITS_ONE
# )
# ser.setDTR(False)
# ser.setRTS(False)

# if not ser.is_open:
#     ser.open()

async def echo(queue, websocket):
    #print("enter")
    while True and websocket.open:
        message = await queue.get()
        #print(message)
        await websocket.send(message)
        # msg = ser.readline().decode()
        # print(msg)
        # await websocket.send(msg)
    #print("exit")

async def start_socket(queue):
    print("Start socket")
    async with websockets.serve(functools.partial(echo, queue), "localhost", 8765):
        print("HELLO")
        await asyncio.Future()

def blocking(loop, queue):

    # while True:
    #     data = ser.readline().decode()
    #     #print(data)
    #     loop.call_soon_threadsafe(queue.put_nowait, data)

    cap = cv2.VideoCapture(0) # use VideoCapture(0) to use local (built in) webcam
    # cap = cv2.VideoCapture(1) # use VideoCapture(1) to use a USB webcam
    
    mpHands = mp.solutions.hands
    hands = mpHands.Hands(static_image_mode=False,
                        max_num_hands=2,
                        min_detection_confidence=0.5,
                        min_tracking_confidence=0.5)
    mpDraw = mp.solutions.drawing_utils

    pTime = 0
    cTime = 0

    while True:
        success, img = cap.read()
        img = cv2.flip(img, 1)
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = hands.process(imgRGB)
        # print(results.multi_hand_landmarks)

        if results.multi_hand_landmarks:
            for handLms in results.multi_hand_landmarks:
                for id, lm in enumerate(handLms.landmark):
                    #print(id,lm)
                    h, w, c = img.shape
                    cx, cy = int(lm.x *100), int(lm.y*100)
                    if id == 8:
                        # to get the purple line that tracks the index finger, uncomment the following two lines
                        # cv2.circle(img, (cx,cy), 3, (255,0,255), cv2.FILLED)
                        # cv2.line(img, (0,0), (cx,cy), (255,0,255), 3)
                        # print(cx, cy)
                        message = str(cx)+' '+str(cy)
                        print(message)
                        loop.call_soon_threadsafe(queue.put_nowait, message)

                mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)

        # cTime = time.time()
        # fps = 1/(cTime-pTime)
        # pTime = cTime

        # cv2.putText(img,str(int(fps)), (10,70), cv2.FONT_HERSHEY_PLAIN, 3, (255,0,255), 3)

        cv2.imshow("Image", img)
        cv2.waitKey(1)

async def main():
    queue = asyncio.Queue()
    fake_queue = asyncio.Queue()
    loop = asyncio.get_running_loop()

    blocking_fut = loop.run_in_executor(None, blocking, loop, queue)
    # nonblocking_task1 = loop.create_task(start_socket(queue))
    nonblocking_task2 = loop.create_task(start_socket(queue))

    running = True  # use whatever exit condition
    while running:
        await fake_queue.get()
       
asyncio.run(main())