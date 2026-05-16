import random

from ..models.unit import Unit
from ..models.hero import Hero
from ..systems.luck import apply_luck


def get_base_damage(unit: Unit) -> int:
    return random.randint(unit.min_damage, unit.max_damage)


def get_skill_bonus(hero: Hero, skill_name: str) -> int:
    return hero.get_skill(skill_name)


def skill_level_to_bonus(level: int, basic: float, advanced: float, expert: float) -> float:
    bonuses = {
        0: 0.0,
        1: basic,
        2: advanced,
        3: expert,
    }
    return bonuses.get(level, 0.0)


def apply_damage(
    attacker: Unit,
    defender: Unit,
    att_hero: Hero,
    def_hero: Hero,
    is_ranged: bool = False,
    distance: int = 1,
) -> int:
    base_damage = get_base_damage(attacker)

    attacker_attack = attacker.attack + att_hero.attack_skill
    defender_defense = defender.defense + def_hero.defense_skill

    attack_diff = attacker_attack - defender_defense
    defense_diff = defender_defense - attacker_attack

    attack_bonus = max(0.0, 0.05 * attack_diff)
    defense_reduction = max(0.0, 0.025 * defense_diff)

    if is_ranged:
        skill_level = get_skill_bonus(att_hero, "Archery")
        skill_bonus = skill_level_to_bonus(skill_level, 0.10, 0.25, 0.50)
    else:
        skill_level = get_skill_bonus(att_hero, "Offense")
        skill_bonus = skill_level_to_bonus(skill_level, 0.10, 0.20, 0.30)

    armorer_level = get_skill_bonus(def_hero, "Armorer")
    armorer_reduction = skill_level_to_bonus(armorer_level, 0.05, 0.10, 0.15)

    range_reduction = 0.5 if is_ranged and distance > 6 else 0.0

    modifier = (
    (1 + attack_bonus + skill_bonus)
    * apply_luck(att_hero)
    * (1 - defense_reduction)
    * (1 - armorer_reduction)
    * (1 - range_reduction)
    )

    modifier = max(0.1, min(modifier, 4.0))

    return max(1, int(base_damage * modifier))