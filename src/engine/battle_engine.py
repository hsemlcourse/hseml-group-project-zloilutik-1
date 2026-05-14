import random

from ..models.army import Army
from ..models.hero import Hero
from ..systems.damage import apply_damage
from ..systems.morale import calculate_morale, morale_trigger
from ..systems.battlefield import BattleField


class BattleEngine:

    def __init__(self, army_a: Army, army_b: Army, hero_a: Hero, hero_b: Hero):
        self.a = army_a
        self.b = army_b
        self.hero_a = hero_a
        self.hero_b = hero_b

        self.field = BattleField()
        self.field.place_army(self.a, "A")
        self.field.place_army(self.b, "B")

    def all_units(self):
        return self.a.alive_units() + self.b.alive_units()

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

    def step(self):

        for unit in sorted(self.all_units(), key=lambda u: u.speed, reverse=True):

            if unit.count <= 0:
                continue

            enemy_army = self.b if unit in self.a.units else self.a
            enemies = enemy_army.alive_units()

            if not enemies:
                return

            target = random.choice(enemies)

            att_hero = self.hero_a if unit in self.a.units else self.hero_b
            def_hero = self.hero_b if unit in self.a.units else self.hero_a

            distance = self.field.distance(unit, target)

            damage = apply_damage(
                attacker=unit,
                defender=target,
                att_hero=att_hero,
                def_hero=def_hero,
                distance=distance,
                is_ranged=False
            )

            self.apply_stack_damage(target, damage)

            morale = calculate_morale(self.a if unit in self.a.units else self.b)

            if morale_trigger(morale) and target.count > 0:
                extra_damage = apply_damage(
                    attacker=unit,
                    defender=target,
                    att_hero=att_hero,
                    def_hero=def_hero,
                    distance=distance,
                    is_ranged=False
                )

                self.apply_stack_damage(target, extra_damage)

    def battle(self):
        rounds = 0

        while not self.a.is_defeated() and not self.b.is_defeated():
            self.step()
            rounds += 1

        return {
            "winner": "A" if not self.a.is_defeated() else "B",
            "rounds": rounds
        }