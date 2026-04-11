import random

REST_ANGLE = 180


def wave() -> str:
    count = random.randint(2, 4)
    angle = REST_ANGLE - random.randint(15, 30)
    hold = random.randint(100, 300)
    steps = []
    for _ in range(count):
        steps.append(f"{angle},{hold}")
        steps.append(f"{REST_ANGLE},{hold}")
    return ";".join(steps)


def love() -> str:
    angle = REST_ANGLE - random.randint(60, 75)
    hold = random.randint(600, 900)
    return f"{angle},{hold}"


def sad() -> str:
    angle = REST_ANGLE - random.randint(10, 18)
    hold = random.randint(1500, 2500)
    return f"{angle},{hold}"
