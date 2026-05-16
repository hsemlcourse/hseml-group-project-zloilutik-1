import random

from ..models.unit import Unit
from ..models.hero import Hero
from ..systems.luck import apply_luck


def get_base_damage(unit: Unit) -> int:
    return random.randint(unit.min_damage, unit.max_damage)


def get_skill_bonus(hero: Hero, skill_name: str) -> int:
    return hero.get_skill(skill_name)


def skill_level_to_bonus(
    level: int,
    basic: float,
    advanced: float,
    expert: float
) -> float:
    bonuses = {
        0: 0.0,
        1: basic,
        2: advanced,
        3: expert,
    }

    return bonuses.get(level, 0.0)


def calculate_attack_bonus(
    attacker: Unit,
    defender: Unit,
    att_hero: Hero,
    def_hero: Hero
) -> float:
    attacker_attack = attacker.attack + att_hero.attack_skill
    defender_defense = defender.defense + def_hero.defense_skill

    diff = attacker_attack - defender_defense

    if diff <= 0:
        return 0.0

    return 0.05 * diff


def calculate_defense_reduction(
    attacker: Unit,
    defender: Unit,
    att_hero: Hero,
    def_hero: Hero
) -> float:
    attacker_attack = attacker.attack + att_hero.attack_skill
    defender_defense = defender.defense + def_hero.defense_skill

    diff = defender_defense - attacker_attack

    if diff <= 0:
        return 0.0

    return 0.025 * diff


def calculate_skill_bonus(
    attacker: Unit,
    att_hero: Hero,
    is_ranged: bool
) -> float:
    if is_ranged:
        level = get_skill_bonus(att_hero, "Archery")
        return skill_level_to_bonus(level, 0.10, 0.25, 0.50)

    level = get_skill_bonus(att_hero, "Offense")
    return skill_level_to_bonus(level, 0.10, 0.20, 0.30)


def calculate_armorer_reduction(def_hero: Hero) -> float:
    level = get_skill_bonus(def_hero, "Armorer")
    return skill_level_to_bonus(level, 0.05, 0.10, 0.15)


def calculate_range_reduction(
    is_ranged: bool,
    distance: int
) -> float:
    if is_ranged and distance > 6:
        return 0.5

    return 0.0


def clamp_modifier(value: float) -> float:
    return max(0.1, min(value, 4.0))


def apply_damage(
    attacker: Unit,
    defender: Unit,
    att_hero: Hero,
    def_hero: Hero,
    is_ranged: bool = False,
    distance: int = 1,
) -> int:
    base_damage = get_base_damage(attacker)

    attack_bonus = calculate_attack_bonus(
        attacker,
        defender,
        att_hero,
        def_hero
    )

    defense_reduction = calculate_defense_reduction(
        attacker,
        defender,
        att_hero,
        def_hero
    )

    skill_bonus = calculate_skill_bonus(
        attacker,
        att_hero,
        is_ranged
    )

    armorer_reduction = calculate_armorer_reduction(def_hero)

    range_reduction = calculate_range_reduction(
        is_ranged,
        distance
    )

    modifier = (
        (1 + attack_bonus + skill_bonus)
        * apply_luck(att_hero)
        * (1 - defense_reduction)
        * (1 - armorer_reduction)
        * (1 - range_reduction)
    )

    modifier = clamp_modifier(modifier)

    return max(1, int(base_damage * modifier))