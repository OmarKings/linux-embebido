import time
import serial
import sys
from serial.tools import list_ports

# Supported baud rates
BAUDRATES = [
    110, 300, 600, 1200, 2400, 4800, 9600, 14400,
    19200, 28800, 38400, 57600, 115200, 230400,
    256000, 460800, 560000, 921600, 128000, 153600
]

class SerialDevice:
    """
    Wrapper around pyserial's Serial
    """
    def __init__(self, port: str, baudrate: int, timeout: float = 2.0):
        if baudrate not in BAUDRATES:
            raise ValueError(f"Baudrate not supported: {baudrate}")
        try:
            self.serial = serial.Serial(
                port=port,
                baudrate=baudrate,
                timeout=timeout
            )
            # give the device time to initialize
            time.sleep(2)
        except serial.SerialException as e:
            raise RuntimeError(f"Unable to open serial port: {e}")

    @staticmethod
    def find_available_ports() -> list[str]:
        """
        Returns a list of available serial port names on the system.
        """
        return [p.device for p in list_ports.comports()]

    def write(self, data: bytes) -> None:
        """
        Write raw bytes to the serial device.
        """
        self.serial.write(data)

    def read_line(self) -> bytes:
        """
        Read a single line (ending with newline) from the device.
        """
        return self.serial.readline()

    def close(self) -> None:
        """
        Close the serial connection.
        """
        if self.serial.is_open:
            self.serial.close()


def main():
    # List and select ports
    ports = SerialDevice.find_available_ports()
    if not ports:
        print("No serial ports found. Exiting.")
        sys.exit(1)

    print("Available ports:")
    for i, p in enumerate(ports):
        print(f"  {i}: {p}")

    choice = input("Select port index (default 0): ").strip()
    port = ports[int(choice)] if choice.isdigit() and int(choice) < len(ports) else ports[0]
    baud = input(f"Enter baud rate (default {9600}): ").strip()
    baud = int(baud) if baud.isdigit() else 9600

    # Initialize device
    try:
        dev = SerialDevice(port, baud)
    except Exception as e:
        print(e)
        sys.exit(1)

    # Handshake
    dev.write(b"Connect\n")
    response = dev.read_line()
    print("Handshake response:", response.decode('utf-8', errors='ignore').strip())

    # Interactive loop
    try:
        while True:
            to_send = input("Enter a message to send (Ctrl+C to exit): ")
            dev.write(to_send.encode('utf-8') + b"\n")
            time.sleep(0.1)
            incoming = dev.read_line()
            print("Received:", incoming.decode('utf-8', errors='ignore').strip())
    except KeyboardInterrupt:
        print("Exiting...")
    finally:
        dev.close()


if __name__ == '__main__':
    main()
