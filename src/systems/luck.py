import random

from ..models.hero import Hero


def apply_luck(hero: Hero) -> float:

    luck_level = hero.get_skill("luck")

    good_chance = 0.10

    if luck_level == 1:
        good_chance += 0.05

    elif luck_level == 2:
        good_chance += 0.10

    elif luck_level == 3:
        good_chance += 0.15

    bad_chance = 0.05

    roll = random.random()

    if roll < good_chance:
        return 1.5

    if roll > 1 - bad_chance:
        return 0.5

    return 1.0