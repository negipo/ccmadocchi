import re
from unittest.mock import patch

from ccmadocchi.motions import love, sad, wave

STEP_PATTERN = re.compile(r"^\d{1,3},\d+$")
REST_ANGLE = 45


def _parse_steps(command: str) -> list[tuple[int, int]]:
    return [
        (int(p.split(",")[0]), int(p.split(",")[1]))
        for p in command.split(";")
    ]


class TestWave:
    @patch("ccmadocchi.motions.random.randint")
    def test_wave_generates_oscillation_steps(self, mock_randint):
        mock_randint.side_effect = [3, 15, 200, 10, 150, 20, 250]
        result = wave()
        steps = _parse_steps(result)
        assert len(steps) == 6
        assert steps[0] == (30, 200)
        assert steps[1] == (45, 200)
        assert steps[2] == (35, 150)
        assert steps[3] == (45, 150)
        assert steps[4] == (25, 250)
        assert steps[5] == (45, 250)

    def test_wave_format_is_valid(self):
        result = wave()
        for step in result.split(";"):
            assert STEP_PATTERN.match(step), f"invalid step format: {step}"

    def test_wave_angles_in_range(self):
        for _ in range(50):
            steps = _parse_steps(wave())
            for angle, hold in steps:
                assert 0 <= angle <= 180


class TestLove:
    @patch("ccmadocchi.motions.random.randint")
    def test_love_generates_single_step(self, mock_randint):
        mock_randint.side_effect = [45, 1000]
        result = love()
        steps = _parse_steps(result)
        assert len(steps) == 1
        assert steps[0] == (0, 1000)

    def test_love_angle_in_range(self):
        for _ in range(50):
            steps = _parse_steps(love())
            angle, hold = steps[0]
            assert 0 <= angle <= 180
            assert 800 <= hold <= 1200


class TestSad:
    @patch("ccmadocchi.motions.random.randint")
    def test_sad_generates_single_step(self, mock_randint):
        mock_randint.side_effect = [10, 2000]
        result = sad()
        steps = _parse_steps(result)
        assert len(steps) == 1
        assert steps[0] == (35, 2000)

    def test_sad_angle_in_range(self):
        for _ in range(50):
            steps = _parse_steps(sad())
            angle, hold = steps[0]
            assert 0 <= angle <= 180
            assert 1500 <= hold <= 2500
