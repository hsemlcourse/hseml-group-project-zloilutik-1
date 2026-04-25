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

    def all_units(self):
        return self.a.alive_units() + self.b.alive_units()

    def step(self):

        for unit in sorted(self.all_units(), key=lambda u: u.speed, reverse=True):

            enemy_army = self.b if unit in self.a.units else self.a
            enemies = enemy_army.alive_units()

            if not enemies:
                return

            target = random.choice(enemies)

            att_hero = self.hero_a if unit in self.a.units else self.hero_b
            def_hero = self.hero_b if unit in self.a.units else self.hero_a

            damage = apply_damage(unit, target, att_hero, def_hero)

            # apply damage (упрощённо)
            while damage > 0 and target.count > 0:
                if damage >= target.hp:
                    damage -= target.hp
                    target.count -= 1
                else:
                    target.hp -= damage
                    damage = 0

            morale = calculate_morale(self.a if unit in self.a.units else self.b)

            if morale_trigger(morale):
                # bonus attack
                pass

    def battle(self):
        rounds = 0

        while not self.a.is_defeated() and not self.b.is_defeated():
            self.step()
            rounds += 1

        return "A" if not self.a.is_defeated() else "B"