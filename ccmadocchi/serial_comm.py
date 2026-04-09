import time

import serial
import serial.tools.list_ports


def find_serial_port() -> str | None:
    ports = serial.tools.list_ports.comports()
    for port in ports:
        if "usbmodem" in port.device or "usbserial" in port.device:
            return port.device
    return None


def send_command(port: str, command: str) -> None:
    with serial.Serial(port, 9600, timeout=10) as ser:
        time.sleep(2)
        ser.write(command.encode())
        ser.read(1)
