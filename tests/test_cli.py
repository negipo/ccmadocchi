from unittest.mock import patch

from click.testing import CliRunner

from ccmadocchi.cli import main


class TestWaveCommand:
    @patch("ccmadocchi.cli.send_command")
    @patch("ccmadocchi.cli.find_serial_port", return_value="/dev/cu.usbmodem1234")
    def test_wave_sends_command(self, mock_find, mock_send):
        runner = CliRunner()
        result = runner.invoke(main, ["wave"])

        assert result.exit_code == 0
        mock_send.assert_called_once_with("/dev/cu.usbmodem1234", "w")

    @patch("ccmadocchi.cli.find_serial_port", return_value=None)
    def test_wave_fails_when_no_device(self, mock_find):
        runner = CliRunner()
        result = runner.invoke(main, ["wave"])

        assert result.exit_code != 0
        assert "見つかりません" in result.output

    @patch("ccmadocchi.cli.send_command")
    def test_wave_with_explicit_port(self, mock_send):
        runner = CliRunner()
        result = runner.invoke(main, ["wave", "--port", "/dev/ttyUSB0"])

        assert result.exit_code == 0
        mock_send.assert_called_once_with("/dev/ttyUSB0", "w")
