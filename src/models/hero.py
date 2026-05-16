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

    def get_skill(self, skill_name: str) -> int:
        skill_name = skill_name.strip().lower()

        if self.skill_1_name.strip().lower() == skill_name:
            return self.skill_1_level

        if self.skill_2_name.strip().lower() == skill_name:
            return self.skill_2_level

        return 0