from dataclasses import dataclass

@dataclass
class Hero:
    name: str
    faction: str
    attack_skill: int
    defense_skill: int
    skill_1_name: str
    skill_1_level: int
    skill_2_name: str
    skill_2_level: int