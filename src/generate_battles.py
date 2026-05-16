import random
from pathlib import Path

import pandas as pd

from src.army_generator import generate_army, load_units
from src.engine.battle_engine import BattleEngine
from src.hero_generator import generate_hero, load_heroes

RANDOM_SEED = 42


def army_features(army, prefix: str) -> dict:
    return {
        f"{prefix}_stacks": army.stacks_count(),
        f"{prefix}_total_units": army.total_units(),
        f"{prefix}_total_health": army.total_health(),
        f"{prefix}_total_attack": army.total_attack(),
        f"{prefix}_total_defense": army.total_defense(),
        f"{prefix}_total_damage_min": army.total_damage_min(),
        f"{prefix}_total_damage_max": army.total_damage_max(),
        f"{prefix}_avg_speed": army.avg_speed(),
        f"{prefix}_ranged_stacks": army.ranged_stacks(),
    }


def hero_features(hero, prefix: str) -> dict:
    return {
        f"{prefix}_faction": hero.faction,
        f"{prefix}_attack_skill": hero.attack_skill,
        f"{prefix}_defense_skill": hero.defense_skill,
        f"{prefix}_offense": hero.get_skill("Offense"),
        f"{prefix}_archery": hero.get_skill("Archery"),
        f"{prefix}_armorer": hero.get_skill("Armorer"),
        f"{prefix}_luck": hero.get_skill("Luck"),
    }


def generate_one_battle(units_df, heroes_df) -> dict:
    factions = heroes_df["faction"].dropna().unique().tolist()

    faction_a = random.choice(factions)
    faction_b = random.choice(factions)

    hero_a = generate_hero(heroes_df, faction_a)
    hero_b = generate_hero(heroes_df, faction_b)

    army_a = generate_army(hero_a.faction, units_df)
    army_b = generate_army(hero_b.faction, units_df)

    row = {}

    row.update(hero_features(hero_a, "hero_a"))
    row.update(hero_features(hero_b, "hero_b"))

    row.update(army_features(army_a, "army_a"))
    row.update(army_features(army_b, "army_b"))

    engine = BattleEngine(
        army_a=army_a,
        army_b=army_b,
        hero_a=hero_a,
        hero_b=hero_b
    )

    result = engine.battle()

    row["rounds"] = result["rounds"]
    row["winner"] = result["winner"]

    if result["winner"] == "A":
        row["target"] = 1
    elif result["winner"] == "B":
        row["target"] = 0
    else:
        row["target"] = -1

    return row


def generate_battles(n_battles: int = 10000) -> pd.DataFrame:
    random.seed(RANDOM_SEED)

    units_df = load_units(
        "data/raw/Heroes of Might and Magic 3 Units.csv"
    )

    heroes_df = load_heroes(
        "data/raw/Heroes of Might and Magic 3 Heroes.csv"
    )

    rows = []

    for i in range(n_battles):
        row = generate_one_battle(units_df, heroes_df)
        rows.append(row)

        if (i + 1) % 1000 == 0:
            print(f"Generated {i + 1} battles")

    return pd.DataFrame(rows)


if __name__ == "__main__":
    output_path = Path("data/processed/battles_dataset.csv")
    output_path.parent.mkdir(parents=True, exist_ok=True)

    df = generate_battles(n_battles=10000)

    df.to_csv(output_path, index=False)

    print("Shape:", df.shape)
    print(df["winner"].value_counts())
    print(df.head())