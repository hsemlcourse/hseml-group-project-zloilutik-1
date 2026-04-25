from dataclasses import dataclass


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