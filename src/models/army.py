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