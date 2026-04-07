from unittest.mock import MagicMock, patch

from ccmadocchi.serial_comm import find_serial_port, send_command


class TestSendCommand:
    @patch("ccmadocchi.serial_comm.serial.Serial")
    def test_send_wave_command(self, mock_serial_class):
        mock_serial = MagicMock()
        mock_serial_class.return_value.__enter__ = MagicMock(return_value=mock_serial)
        mock_serial_class.return_value.__exit__ = MagicMock(return_value=False)

        send_command("/dev/ttyUSB0", "w")

        mock_serial_class.assert_called_once_with("/dev/ttyUSB0", 9600, timeout=2)
        mock_serial.write.assert_called_once_with(b"w")


class TestFindSerialPort:
    @patch("ccmadocchi.serial_comm.serial.tools.list_ports.comports")
    def test_find_port_returns_first_match(self, mock_comports):
        mock_port = MagicMock()
        mock_port.device = "/dev/cu.usbmodem1234"
        mock_port.description = "Maker Nano"
        mock_comports.return_value = [mock_port]

        result = find_serial_port()

        assert result == "/dev/cu.usbmodem1234"

    @patch("ccmadocchi.serial_comm.serial.tools.list_ports.comports")
    def test_find_port_returns_none_when_empty(self, mock_comports):
        mock_comports.return_value = []

        result = find_serial_port()

        assert result is None
