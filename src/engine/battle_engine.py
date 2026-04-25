import random

from ..models.army import Army
from ..models.hero import Hero

from ..systems.damage import apply_damage
from ..systems.morale import calculate_morale, morale_trigger


class BattleEngine:

    def __init__(self, army_a: Army, army_b: Army, hero_a: Hero, hero_b: Hero):
        self.a = army_a
        self.b = army_b
        self.hero_a = hero_a
        self.hero_b = hero_b

    # =========================
    # ALL UNITS
    # =========================
    def all_units(self):
        return self.a.alive_units() + self.b.alive_units()

    # =========================
    # STACK DAMAGE 
    # =========================
    def apply_stack_damage(self, target, damage: int):

        if damage <= 0 or target.count <= 0:
            return

        kills = damage // target.hp
        remainder = damage % target.hp

        target.count -= kills

        if target.count <= 0:
            target.count = 0
            return

        if remainder > 0:
            target.count -= 1

            if target.count <= 0:
                target.count = 0

    # =========================
    # STEP
    # =========================
    def step(self):

        turn_order = sorted(
            self.all_units(),
            key=lambda u: u.speed,
            reverse=True
        )

        for unit in turn_order:

            if unit.count <= 0:
                continue

            enemy_army = self.b if unit in self.a.units else self.a
            enemies = enemy_army.alive_units()

            if not enemies:
                return

            target = random.choice(enemies)

            att_hero = self.hero_a if unit in self.a.units else self.hero_b
            def_hero = self.hero_b if unit in self.a.units else self.hero_a

            damage = apply_damage(unit, target, att_hero, def_hero)
            self.apply_stack_damage(target, damage)

            morale = calculate_morale(self.a if unit in self.a.units else self.b)

            if morale_trigger(morale):

                extra_damage = apply_damage(unit, target, att_hero, def_hero)
                self.apply_stack_damage(target, extra_damage)

    # =========================
    # BATTLE LOOP
    # =========================
    def battle(self):

        rounds = 0

        while not self.a.is_defeated() and not self.b.is_defeated():

            self.step()
            rounds += 1

        winner = "A" if not self.a.is_defeated() else "B"

        return {
            "winner": winner,
            "rounds": rounds
        }