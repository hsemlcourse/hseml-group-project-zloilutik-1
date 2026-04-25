import random
from ..models.unit import Unit
from ..models.hero import Hero


def get_base_damage(unit: Unit):
    return random.randint(unit.min_damage, unit.max_damage)


def apply_damage(attacker: Unit, defender: Unit, att_hero: Hero, def_hero: Hero):

    base = get_base_damage(attacker)

    i1 = 0.05 * (
        (attacker.attack + att_hero.attack_skill)
        - (defender.defense + def_hero.defense_skill)
    )

    i1 = max(0, i1)

    luck = 1.5 if random.random() < 0.1 else 1.0

    modifier = (1 + i1) * luck

    return int(base * modifier)