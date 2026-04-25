import random

def apply_luck():
    roll = random.random()

    if roll < 0.1:
        return 1.5
    elif roll > 0.9:
        return 0.5
    return 1.0