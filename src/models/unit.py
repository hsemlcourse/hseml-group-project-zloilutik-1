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

    x: int = 0
    y: int = 0

    def total_hp(self):
        return self.hp * self.count

    def is_alive(self) -> bool:
        return self.count > 0