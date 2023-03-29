import asyncio
import websockets
import serial

ser = serial.Serial(
    port="/dev/cu.ESP32", baudrate=115200, bytesize=8, timeout=1, stopbits=serial.STOPBITS_ONE
)
ser.setDTR(False)
ser.setRTS(False)

if not ser.is_open:
    ser.open()


async def handler(websocket, path):
    print("open socket")

    while True and websocket.open and ser.open:
        msg = ser.readline().decode()
        if (msg != ""):
            print(msg)
            await websocket.send(msg)


       

async def main():
    async with websockets.serve(handler, "localhost", 8766):
        await asyncio.Future()  # run forever
       
if __name__ == "__main__":
    asyncio.run(main())