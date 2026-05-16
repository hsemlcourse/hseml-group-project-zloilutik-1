from dataclasses import dataclass
from typing import List

from .unit import Unit


@dataclass
class Army:
    units: List[Unit]

    def alive_units(self):
        return [u for u in self.units if u.count > 0]

    def is_defeated(self):
        return len(self.alive_units()) == 0

    def total_units(self):
        return sum(u.count for u in self.units)

    def total_health(self):
        return sum(u.hp * u.count for u in self.units)

    def total_attack(self):
        return sum(u.attack * u.count for u in self.units)

    def total_defense(self):
        return sum(u.defense * u.count for u in self.units)

    def total_damage_min(self):
        return sum(u.min_damage * u.count for u in self.units)

    def total_damage_max(self):
        return sum(u.max_damage * u.count for u in self.units)

    def avg_speed(self):
        if not self.units:
            return 0
        return sum(u.speed for u in self.units) / len(self.units)

    def ranged_stacks(self):
        return sum(1 for u in self.units if u.is_ranged)

    def stacks_count(self):
        return len(self.units)