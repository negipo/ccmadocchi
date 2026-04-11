import random

REST_ANGLE = 180

WAVE_ANGLE_RANGE = (30, 45)
WAVE_COUNT_RANGE = (2, 4)
LOVE_ANGLE_RANGE = (60, 75)
SAD_ANGLE_RANGE = (10, 18)


def _validate_range(value: int, min_val: int, max_val: int, name: str) -> None:
    if not (min_val <= value <= max_val):
        raise ValueError(f"{name}は{min_val}-{max_val}の範囲で指定してください: {value}")


def wave(angle: int | None = None, count: int | None = None) -> str:
    if count is None:
        count = random.randint(*WAVE_COUNT_RANGE)
    else:
        _validate_range(count, *WAVE_COUNT_RANGE, "count")
    if angle is None:
        angle = random.randint(*WAVE_ANGLE_RANGE)
    else:
        _validate_range(angle, *WAVE_ANGLE_RANGE, "angle")
    hold = random.randint(100, 300)
    steps = []
    for _ in range(count):
        steps.append(f"{REST_ANGLE - angle},{hold}")
        steps.append(f"{REST_ANGLE},{hold}")
    return ";".join(steps)


def love(angle: int | None = None) -> str:
    if angle is None:
        angle = random.randint(*LOVE_ANGLE_RANGE)
    else:
        _validate_range(angle, *LOVE_ANGLE_RANGE, "angle")
    hold = random.randint(600, 900)
    return f"{REST_ANGLE - angle},{hold}"


def sad(angle: int | None = None) -> str:
    if angle is None:
        angle = random.randint(*SAD_ANGLE_RANGE)
    else:
        _validate_range(angle, *SAD_ANGLE_RANGE, "angle")
    hold = random.randint(1500, 2500)
    return f"{REST_ANGLE - angle},{hold}"
