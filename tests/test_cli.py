from unittest.mock import patch

from click.testing import CliRunner

from ccmadocchi.cli import main


class TestYoCommand:
    @patch("ccmadocchi.cli.send_command")
    @patch("ccmadocchi.cli.yo_motion", return_value="145,200;180,200")
    @patch("ccmadocchi.cli.find_serial_port", return_value="/dev/cu.usbmodem1234")
    def test_yo_sends_generated_command(self, mock_find, mock_motion, mock_send):
        runner = CliRunner()
        result = runner.invoke(main, ["yo"])

        assert result.exit_code == 0
        mock_motion.assert_called_once_with(angle=None, hold=None)
        mock_send.assert_called_once_with("/dev/cu.usbmodem1234", "145,200;180,200")
        assert "yo送信" in result.output

    @patch("ccmadocchi.cli.send_command")
    @patch("ccmadocchi.cli.yo_motion", return_value="145,200;180,200")
    @patch("ccmadocchi.cli.find_serial_port", return_value="/dev/cu.usbmodem1234")
    def test_yo_silent_suppresses_output(self, mock_find, mock_motion, mock_send):
        runner = CliRunner()
        result = runner.invoke(main, ["yo", "--silent"])

        assert result.exit_code == 0
        assert result.output == ""


class TestWaveCommand:
    @patch("ccmadocchi.cli.send_command")
    @patch("ccmadocchi.cli.wave_motion", return_value="145,200;180,200")
    @patch("ccmadocchi.cli.find_serial_port", return_value="/dev/cu.usbmodem1234")
    def test_wave_sends_generated_command(self, mock_find, mock_motion, mock_send):
        runner = CliRunner()
        result = runner.invoke(main, ["wave"])

        assert result.exit_code == 0
        mock_motion.assert_called_once_with(angle=None, count=None, hold=None)
        mock_send.assert_called_once_with("/dev/cu.usbmodem1234", "145,200;180,200")

    @patch("ccmadocchi.cli.find_serial_port", return_value=None)
    def test_wave_fails_when_no_device(self, mock_find):
        runner = CliRunner()
        result = runner.invoke(main, ["wave"])

        assert result.exit_code != 0
        assert "見つかりません" in result.output

    @patch("ccmadocchi.cli.send_command")
    @patch("ccmadocchi.cli.wave_motion", return_value="145,200;180,200")
    def test_wave_with_explicit_port(self, mock_motion, mock_send):
        runner = CliRunner()
        result = runner.invoke(main, ["wave", "--port", "/dev/ttyUSB0"])

        assert result.exit_code == 0
        mock_send.assert_called_once_with("/dev/ttyUSB0", "145,200;180,200")

    @patch("ccmadocchi.cli.send_command")
    @patch("ccmadocchi.cli.wave_motion", return_value="140,200;180,200")
    @patch("ccmadocchi.cli.find_serial_port", return_value="/dev/cu.usbmodem1234")
    def test_wave_with_angle_and_count(self, mock_find, mock_motion, mock_send):
        runner = CliRunner()
        result = runner.invoke(main, ["wave", "--angle", "40", "--count", "2"])

        assert result.exit_code == 0
        mock_motion.assert_called_once_with(angle=40, count=2, hold=None)

    @patch("ccmadocchi.cli.find_serial_port", return_value="/dev/cu.usbmodem1234")
    def test_wave_fails_with_out_of_range_angle(self, mock_find):
        runner = CliRunner()
        result = runner.invoke(main, ["wave", "--angle", "100"])

        assert result.exit_code != 0


class TestLoveCommand:
    @patch("ccmadocchi.cli.send_command")
    @patch("ccmadocchi.cli.love_motion", return_value="115,800")
    @patch("ccmadocchi.cli.find_serial_port", return_value="/dev/cu.usbmodem1234")
    def test_love_sends_generated_command(self, mock_find, mock_motion, mock_send):
        runner = CliRunner()
        result = runner.invoke(main, ["love"])

        assert result.exit_code == 0
        mock_motion.assert_called_once_with(angle=None, hold=None)
        mock_send.assert_called_once_with("/dev/cu.usbmodem1234", "115,800")

    @patch("ccmadocchi.cli.find_serial_port", return_value=None)
    def test_love_fails_when_no_device(self, mock_find):
        runner = CliRunner()
        result = runner.invoke(main, ["love"])

        assert result.exit_code != 0
        assert "見つかりません" in result.output


class TestSadCommand:
    @patch("ccmadocchi.cli.send_command")
    @patch("ccmadocchi.cli.sad_motion", return_value="170,2000")
    @patch("ccmadocchi.cli.find_serial_port", return_value="/dev/cu.usbmodem1234")
    def test_sad_sends_generated_command(self, mock_find, mock_motion, mock_send):
        runner = CliRunner()
        result = runner.invoke(main, ["sad"])

        assert result.exit_code == 0
        mock_motion.assert_called_once_with(angle=None, hold=None)
        mock_send.assert_called_once_with("/dev/cu.usbmodem1234", "170,2000")

    @patch("ccmadocchi.cli.find_serial_port", return_value=None)
    def test_sad_fails_when_no_device(self, mock_find):
        runner = CliRunner()
        result = runner.invoke(main, ["sad"])

        assert result.exit_code != 0
        assert "見つかりません" in result.output
