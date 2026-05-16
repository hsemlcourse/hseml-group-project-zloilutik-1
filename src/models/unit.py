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

    is_ranged: bool = False
    shots: int = 0

    creature_type: str = "living"
    magic_resistance: float = 0.0
    spell_immunity: str = "none"

    x: int = 0
    y: int = 0

    def total_hp(self):
        return self.hp * self.count

    def is_alive(self) -> bool:
        return self.count > 0