import random

REST_ANGLE = 45


def wave() -> str:
    count = random.randint(2, 4)
    angle = REST_ANGLE - random.randint(10, 20)
    hold = random.randint(100, 300)
    steps = []
    for _ in range(count):
        steps.append(f"{angle},{hold}")
        steps.append(f"{REST_ANGLE},{hold}")
    return ";".join(steps)


def love() -> str:
    angle = max(0, REST_ANGLE - random.randint(40, 50))
    hold = random.randint(800, 1200)
    return f"{angle},{hold}"


def sad() -> str:
    angle = REST_ANGLE - random.randint(7, 12)
    hold = random.randint(1500, 2500)
    return f"{angle},{hold}"
