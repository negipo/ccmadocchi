from unittest.mock import patch

from click.testing import CliRunner

from ccmadocchi.cli import main


class TestWaveCommand:
    @patch("ccmadocchi.cli.send_command")
    @patch("ccmadocchi.cli.wave_motion", return_value="30,200;45,200")
    @patch("ccmadocchi.cli.find_serial_port", return_value="/dev/cu.usbmodem1234")
    def test_wave_sends_generated_command(self, mock_find, mock_motion, mock_send):
        runner = CliRunner()
        result = runner.invoke(main, ["wave"])

        assert result.exit_code == 0
        mock_motion.assert_called_once()
        mock_send.assert_called_once_with("/dev/cu.usbmodem1234", "30,200;45,200")

    @patch("ccmadocchi.cli.find_serial_port", return_value=None)
    def test_wave_fails_when_no_device(self, mock_find):
        runner = CliRunner()
        result = runner.invoke(main, ["wave"])

        assert result.exit_code != 0
        assert "見つかりません" in result.output

    @patch("ccmadocchi.cli.send_command")
    @patch("ccmadocchi.cli.wave_motion", return_value="30,200;45,200")
    def test_wave_with_explicit_port(self, mock_motion, mock_send):
        runner = CliRunner()
        result = runner.invoke(main, ["wave", "--port", "/dev/ttyUSB0"])

        assert result.exit_code == 0
        mock_send.assert_called_once_with("/dev/ttyUSB0", "30,200;45,200")


class TestLoveCommand:
    @patch("ccmadocchi.cli.send_command")
    @patch("ccmadocchi.cli.love_motion", return_value="0,1000")
    @patch("ccmadocchi.cli.find_serial_port", return_value="/dev/cu.usbmodem1234")
    def test_love_sends_generated_command(self, mock_find, mock_motion, mock_send):
        runner = CliRunner()
        result = runner.invoke(main, ["love"])

        assert result.exit_code == 0
        mock_motion.assert_called_once()
        mock_send.assert_called_once_with("/dev/cu.usbmodem1234", "0,1000")

    @patch("ccmadocchi.cli.find_serial_port", return_value=None)
    def test_love_fails_when_no_device(self, mock_find):
        runner = CliRunner()
        result = runner.invoke(main, ["love"])

        assert result.exit_code != 0
        assert "見つかりません" in result.output


class TestSadCommand:
    @patch("ccmadocchi.cli.send_command")
    @patch("ccmadocchi.cli.sad_motion", return_value="35,2000")
    @patch("ccmadocchi.cli.find_serial_port", return_value="/dev/cu.usbmodem1234")
    def test_sad_sends_generated_command(self, mock_find, mock_motion, mock_send):
        runner = CliRunner()
        result = runner.invoke(main, ["sad"])

        assert result.exit_code == 0
        mock_motion.assert_called_once()
        mock_send.assert_called_once_with("/dev/cu.usbmodem1234", "35,2000")

    @patch("ccmadocchi.cli.find_serial_port", return_value=None)
    def test_sad_fails_when_no_device(self, mock_find):
        runner = CliRunner()
        result = runner.invoke(main, ["sad"])

        assert result.exit_code != 0
        assert "見つかりません" in result.output
