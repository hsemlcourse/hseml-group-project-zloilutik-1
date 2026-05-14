import random
import pandas as pd

from src.models.hero import Hero


def load_heroes(path: str) -> pd.DataFrame:
    df = pd.read_csv(
        path,
        sep=';',
        engine='python'
    )

    df.columns = df.columns.str.strip().str.lower()

    return df


def parse_skill_level(value) -> int:
    value = str(value).strip().lower()

    levels = {
        "none": 0,
        "nan": 0,
        "basic": 1,
        "advanced": 2,
        "expert": 3,
    }

    return levels.get(value, 0)


def build_hero(row) -> Hero:
    return Hero(
        name=row["name"],
        faction=row["faction"],

        attack_skill=int(row["attack_skill"]),
        defense_skill=int(row["defence_skill"]),

        skill_1_name=str(row["skill_1_name"]),
        skill_1_level=parse_skill_level(row["skill_1_level"]),

        skill_2_name=str(row["skill_2_name"]),
        skill_2_level=parse_skill_level(row["skill_2_level"])
    )


def generate_hero(heroes_df: pd.DataFrame, faction: str | None = None) -> Hero:
    heroes = heroes_df.copy()

    if faction is not None:
        faction = faction.lower()

        heroes = heroes[
            heroes["faction"].str.lower() == faction
        ].copy()

        if heroes.empty:
            raise ValueError(f"No heroes found for faction: {faction}")

    row = heroes.sample(n=1).iloc[0]

    return build_hero(row)


if __name__ == "__main__":

    heroes = load_heroes(
        "data/raw/Heroes of Might and Magic 3 Heroes.csv"
    )

    hero = generate_hero(heroes)

    print("SELECTED HERO:")
    print(hero)