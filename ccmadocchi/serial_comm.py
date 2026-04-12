import time

import serial
import serial.tools.list_ports


def find_serial_port() -> str | None:
    ports = serial.tools.list_ports.comports()
    for port in ports:
        if "usbmodem" in port.device or "usbserial" in port.device:
            return port.device
    return None


def send_command(port: str, command: str, *, debug: bool = False) -> None:
    with serial.Serial(port, 9600, timeout=10) as ser:
        time.sleep(2)
        payload = f"D:{command}" if debug else command
        ser.write(f"{payload}\n".encode())
        ser.read(1)
