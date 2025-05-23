import time 
import serial 
import os
import sys
#serial_device = serial.Serial()

BAUDRATES =[
300,1200,14400,
115200,600,2400,
19200,230400,4800,
38400,460800,9600,
57600,110,28800,
128000,56000,153600,
256000,921600,
]

class SerialDevice:
    def __init__(self, port:str,baudrate:int):
        if baudrate not in BAUDRATES:
            raise ValueError (f"Baudrate not supported {baudrate}")
        
        self.serial_device = serial.Serial(
            port=port,
        @staticmethod
        def find_avalible_ports()->list[str]:
            if sys.platform.startswith('win'):
                ports = ['COM%s' % (i + 1) for i in range(256)]


SERIAL_PORT = 'COM9'  # Replace with your serial port
BAUD_RATE = 9600
serial_device = serial.Serial(
    port=SERIAL_PORT,
    baudrate=BAUD_RATE,
    #timeout=2  # segundos
)
# Wait for the serial device to initialize
time.sleep(2)
serial_device.write(b"Connect")
message = serial_device.readline()

#Pregunta ; que tipo de mensaje es
print(type(message))
print(message.decode(encoding='utf-8'))

while True:
    try:
        to_send = input("Enter a message to send: ")
        serial_device.write(to_send.encode())
        time.sleep(1)

        message = serial_device.readline()
        print(message.decode(encoding='utf-8'))
    except KeyboardInterrupt:
        print("Exiting...")
        break
serial_device.close()
# Close the serial device

