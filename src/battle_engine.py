import random
from dataclasses import dataclass
from typing import List, Optional


# =========================
# UNIT MODEL
# =========================

@dataclass
class Unit:
    name: str
    faction: str
    speed: int
    attack: int
    defense: int
    hp: int
    count: int
    is_alive: bool = True


    def power(self):
        return self.attack * self.count


# =========================
# HERO ARMY
# =========================

@dataclass
class Army:
    units: List[Unit]

    def alive_units(self):
        return [u for u in self.units if u.is_alive and u.count > 0]

    def is_defeated(self):
        return len(self.alive_units()) == 0


# =========================
# BATTLE FIELD
# =========================

class BattleField:
    def __init__(self, width=5, height=7):
        self.width = width
        self.height = height


# =========================
# INITIATIVE SYSTEM
# =========================

def get_turn_order(all_units: List[Unit]) -> List[Unit]:
    """
    Units act based on speed (higher goes first)
    """
    return sorted(all_units, key=lambda u: u.speed, reverse=True)


# =========================
# MORAL SYSTEM
# =========================

def calculate_morale(army: Army) -> int:
    factions = set(u.faction for u in army.units)

    # undead ignore morale
    if all(u.faction == "Necropolis" for u in army.units):
        return 0

    if len(factions) == 1:
        return 1  # good morale

    if len(factions) == 2:
        return 0  # neutral

    return -1  # bad morale (chaotic army)


def morale_trigger(morale: int) -> bool:
    """
    Simple chance system:
    - good morale -> extra turn chance
    - bad morale -> skip turn chance
    """
    if morale > 0:
        return random.random() < 0.2
    if morale < 0:
        return random.random() < 0.1
    return False


# =========================
# LUCK SYSTEM
# =========================

def apply_luck() -> float:
    """
    Luck modifies damage multiplier
    """
    roll = random.random()

    if roll < 0.1:
        return 1.5  # lucky hit
    elif roll > 0.9:
        return 0.5  # unlucky hit
    return 1.0


# =========================
# DAMAGE
# =========================

def deal_damage(attacker: Unit, defender: Unit):
    base_damage = attacker.attack * attacker.count
    mitigation = defender.defense * 0.5

    damage = max(1, base_damage - mitigation)
    damage *= apply_luck()

    kill = int(damage / defender.hp)

    defender.count -= kill

    if defender.count <= 0:
        defender.is_alive = False
        defender.count = 0


# =========================
# BATTLE ENGINE
# =========================

class BattleEngine:
    def __init__(self, army_a: Army, army_b: Army):
        self.army_a = army_a
        self.army_b = army_b

    def get_all_units(self):
        return self.army_a.alive_units() + self.army_b.alive_units()

    def step(self):
        order = get_turn_order(self.get_all_units())

        for unit in order:
            if not unit.is_alive:
                continue

            enemy_army = self.army_b if unit in self.army_a.units else self.army_a
            enemies = enemy_army.alive_units()

            if not enemies:
                return

            target = random.choice(enemies)

            deal_damage(unit, target)

            # morale extra turn
            morale = calculate_morale(
                self.army_a if unit in self.army_a.units else self.army_b
            )

            if morale_trigger(morale):
                deal_damage(unit, target)

    def battle(self):
        round_num = 0

        while not self.army_a.is_defeated() and not self.army_b.is_defeated():
            self.step()
            round_num += 1

        return {
            "winner": "A" if not self.army_a.is_defeated() else "B",
            "rounds": round_num
        }