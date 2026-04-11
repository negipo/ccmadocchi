import re
from unittest.mock import patch

import pytest

from ccmadocchi.motions import love, sad, wave, yo

STEP_PATTERN = re.compile(r"^\d{1,3},\d+$")
REST_ANGLE = 180


def _parse_steps(command: str) -> list[tuple[int, int]]:
    return [
        (int(p.split(",")[0]), int(p.split(",")[1]))
        for p in command.split(";")
    ]


class TestYo:
    @patch("ccmadocchi.motions.random.randint")
    def test_yo_generates_one_round_trip(self, mock_randint):
        mock_randint.side_effect = [35, 200]
        result = yo()
        steps = _parse_steps(result)
        assert len(steps) == 2
        assert steps[0] == (145, 200)
        assert steps[1] == (180, 200)

    def test_yo_rejects_out_of_range_angle(self):
        with pytest.raises(ValueError):
            yo(angle=50)


class TestWave:
    @patch("ccmadocchi.motions.random.randint")
    def test_wave_generates_oscillation_steps(self, mock_randint):
        mock_randint.side_effect = [3, 35, 200]
        result = wave()
        steps = _parse_steps(result)
        assert len(steps) == 6
        assert steps[0] == (145, 200)
        assert steps[1] == (180, 200)
        assert steps[2] == (145, 200)
        assert steps[3] == (180, 200)
        assert steps[4] == (145, 200)
        assert steps[5] == (180, 200)

    def test_wave_uses_consistent_angle_and_hold(self):
        for _ in range(50):
            steps = _parse_steps(wave())
            angles = [s[0] for s in steps[::2]]
            holds = [s[1] for s in steps]
            assert len(set(angles)) == 1
            assert len(set(holds)) == 1

    def test_wave_format_is_valid(self):
        result = wave()
        for step in result.split(";"):
            assert STEP_PATTERN.match(step), f"invalid step format: {step}"

    def test_wave_angles_in_range(self):
        for _ in range(50):
            steps = _parse_steps(wave())
            for angle, hold in steps:
                assert 0 <= angle <= 180

    @patch("ccmadocchi.motions.random.randint")
    def test_wave_with_fixed_params(self, mock_randint):
        mock_randint.return_value = 200
        result = wave(angle=40, count=2)
        steps = _parse_steps(result)
        assert len(steps) == 4
        assert steps[0] == (140, 200)
        assert steps[1] == (180, 200)

    def test_wave_rejects_out_of_range_angle(self):
        with pytest.raises(ValueError):
            wave(angle=50)

    def test_wave_rejects_out_of_range_count(self):
        with pytest.raises(ValueError):
            wave(count=10)


class TestLove:
    @patch("ccmadocchi.motions.random.randint")
    def test_love_generates_single_step(self, mock_randint):
        mock_randint.side_effect = [65, 800]
        result = love()
        steps = _parse_steps(result)
        assert len(steps) == 1
        assert steps[0] == (115, 800)

    def test_love_angle_in_range(self):
        for _ in range(50):
            steps = _parse_steps(love())
            angle, hold = steps[0]
            assert 0 <= angle <= 180
            assert 600 <= hold <= 900

    def test_love_rejects_out_of_range_angle(self):
        with pytest.raises(ValueError):
            love(angle=80)


class TestSad:
    @patch("ccmadocchi.motions.random.randint")
    def test_sad_generates_single_step(self, mock_randint):
        mock_randint.side_effect = [10, 2000]
        result = sad()
        steps = _parse_steps(result)
        assert len(steps) == 1
        assert steps[0] == (170, 2000)

    def test_sad_angle_in_range(self):
        for _ in range(50):
            steps = _parse_steps(sad())
            angle, hold = steps[0]
            assert 0 <= angle <= 180
            assert 1500 <= hold <= 2500

    def test_sad_rejects_out_of_range_angle(self):
        with pytest.raises(ValueError):
            sad(angle=20)
