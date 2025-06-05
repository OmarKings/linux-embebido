import time
import serial
from serial.tools import list_ports

# Default Caesar cipher shift value
SHIFT = 3


def find_serial_ports():
    """
    Busca y devuelve una lista de puertos seriales disponibles en el sistema.
    """
    return [port.device for port in list_ports.comports()]


def open_connection(port: str, baudrate: int, timeout: float = 2.0) -> serial.Serial:
    """
    Abre una conexión serial con los parámetros indicados y espera un breve tiempo para inicializar.
    """
    try:
        conn = serial.Serial(port=port, baudrate=baudrate, timeout=timeout)
        time.sleep(timeout)
        return conn
    except serial.SerialException as err:
        raise RuntimeError(f"No se pudo abrir {port}: {err}")


def caesar_cipher(text: str, shift: int = SHIFT) -> str:
    """
    Aplica cifrado César sobre texto ASCII, manteniendo mayúsculas, minúsculas y caracteres no alfabéticos.
    """
    result = []
    for char in text:
        if 'A' <= char <= 'Z':
            code = (ord(char) - ord('A') + shift) % 26 + ord('A')
            result.append(chr(code))
        elif 'a' <= char <= 'z':
            code = (ord(char) - ord('a') + shift) % 26 + ord('a')
            result.append(chr(code))
        else:
            result.append(char)
    return ''.join(result)


def main():
    # Listar puertos y elegir uno
    ports = find_serial_ports()
    if not ports:
        print("No se detectaron puertos seriales.")
        return

    for i, p in enumerate(ports):
        print(f"{i}: {p}")
    choice = input("Elige índice de puerto (ENTER para 0): ")
    try:
        port = ports[int(choice)] if choice.isdigit() else ports[0]
    except (ValueError, IndexError):
        port = ports[0]

    baud_input = input("Introduce velocidad [9600]: ")
    baudrate = int(baud_input) if baud_input.isdigit() else 9600

    # Iniciar conexión
    conn = open_connection(port, baudrate)

    # Intercambio inicial
    conn.write("HELLO\n".encode())
    welcome = conn.readline().decode(errors='ignore').strip()
    print("Dispositivo respondió:", welcome)

    try:
        while True:
            text = input("Enviar (Ctrl+C para salir): ")
            # Para cifrar el mensaje con César, descomenta:
            # text = caesar_cipher(text)
            conn.write((text + "\n").encode())
            reply = conn.readline().decode(errors='ignore').strip()
            print("Recibido:", reply)
    except KeyboardInterrupt:
        print("Conexión finalizada por usuario.")
    finally:
        conn.close()


if __name__ == '__main__':
    main()
