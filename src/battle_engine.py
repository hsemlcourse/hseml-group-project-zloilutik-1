import random
from dataclasses import dataclass
from typing import List


# =========================
# UNIT / ARMY
# =========================

@dataclass
class Unit:
    name: str
    faction: str
    speed: int
    attack: int
    defense: int
    min_damage: int
    max_damage: int
    hp: int

    count: int
    is_alive: bool = True

    def total_hp(self):
        return self.hp * self.count


@dataclass
class Army:
    units: List[Unit]

    def alive_units(self):
        return [u for u in self.units if u.count > 0]

    def is_defeated(self):
        return len(self.alive_units()) == 0


# =========================
# FIELD 
# =========================

class BattleField:

    def __init__(self):
        self.h = 11
        self.w = 15

    def get_positions(self, n: int, side: str):
    
        positions = []

        step = self.h // (n + 1)

        for i in range(n):
            y = (i + 1) * step

            if side == "A":
                x = 2
            else:
                x = self.w - 3

            positions.append((x, y))

        return positions


# =========================
# UTILS
# =========================

def clamp(x, a, b):
    return max(a, min(b, x))


def get_base_damage(unit: Unit):
    return random.randint(unit.min_damage, unit.max_damage)


# =========================
# DAMAGE MODEL
# =========================

def calc_i1(att_unit, att_hero, def_unit, def_hero):
    diff = (att_unit.attack + att_hero) - (def_unit.defense + def_hero)

    if diff < 3:
        return 0.0

    return 0.05 * diff


def calc_i2():
    return 0.0   


def calc_i3(i2):
    return 0.05 * i2


def calc_r1(att_unit, att_hero, def_unit, def_hero):
    diff = (def_unit.defense + def_hero) - (att_unit.attack + att_hero)
    return max(0, 0.025 * diff)


def calc_r2():
    return 0.0


def calc_r3():
    return 0.0


def calc_r4():
    return 0.0


def apply_luck():
    return 1.5 if random.random() < 0.1 else 1.0


def apply_damage(attacker, defender, att_hero=0, def_hero=0):
    base = get_base_damage(attacker)

    i1 = calc_i1(attacker, att_hero, defender, def_hero)
    i2 = calc_i2()
    i3 = calc_i3(i2)

    r1 = calc_r1(attacker, att_hero, defender, def_hero)
    r2 = calc_r2()
    r3 = calc_r3()
    r4 = calc_r4()

    luck = apply_luck()

    modifier = (1 + i1 + i2 + i3) * luck * (1 - r1 - r2 - r3 - r4)
    modifier = clamp(modifier, 0.1, 3.0)

    return int(base * modifier)


# =========================
# CORE DAMAGE APPLICATION
# =========================

def deal_damage(attacker: Unit, defender: Unit):
    damage = apply_damage(attacker, defender)

    while damage > 0 and defender.count > 0:

        if damage >= defender.hp:
            damage -= defender.hp
            defender.count -= 1

        else:
            defender.hp -= damage
            damage = 0

    if defender.count <= 0:
        defender.count = 0


# =========================
# MORAL SYSTEM
# =========================

def calculate_morale(army: Army):
    factions = set(u.faction for u in army.units)

    # undead rule
    if all(u.faction == "Necropolis" for u in army.units):
        return 0

    # mixed armies = bad morale
    if len(factions) > 1:
        return -1

    return 1


def morale_trigger(morale):
    if morale > 0:
        return random.random() < 0.2
    if morale < 0:
        return random.random() < 0.1
    return False


# =========================
# INITIATIVE
# =========================

def get_turn_order(units):
    return sorted(units, key=lambda u: u.speed, reverse=True)


# =========================
# BATTLE ENGINE
# =========================

class BattleEngine:
    def __init__(self, army_a: Army, army_b: Army):
        self.a = army_a
        self.b = army_b

    def all_units(self):
        return self.a.alive_units() + self.b.alive_units()

    def step(self):

        for unit in get_turn_order(self.all_units()):

            if unit.count <= 0:
                continue

            enemy_army = self.b if unit in self.a.units else self.a
            enemies = enemy_army.alive_units()

            if not enemies:
                return

            target = random.choice(enemies)

            deal_damage(unit, target)

            morale = calculate_morale(self.a if unit in self.a.units else self.b)

            if morale_trigger(morale):
                deal_damage(unit, target)

    def battle(self):
        rounds = 0

        while not self.a.is_defeated() and not self.b.is_defeated():
            self.step()
            rounds += 1

        return {
            "winner": "A" if not self.a.is_defeated() else "B",
            "rounds": rounds
        }