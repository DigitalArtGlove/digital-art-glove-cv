import serial

ser = serial.Serial(
    port="COM4", baudrate=115200, bytesize=8, timeout=1, stopbits=serial.STOPBITS_ONE
)
ser.setDTR(False)
ser.setRTS(False)

if not ser.is_open:
    ser.open()

while True:
    msg = ser.readline()
    print(msg.decode())