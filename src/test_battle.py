import random

from src.army_generator import generate_army, load_units
from src.engine.battle_engine import BattleEngine
from src.hero_generator import generate_hero, load_heroes


def main():
    units_df = load_units(
        "data/raw/Heroes of Might and Magic 3 Units.csv"
    )

    heroes_df = load_heroes(
        "data/raw/Heroes of Might and Magic 3 Heroes.csv"
    )

    factions = heroes_df["faction"].dropna().unique().tolist()

    faction_a = random.choice(factions)
    faction_b = random.choice(factions)

    hero_a = generate_hero(heroes_df, faction_a)
    hero_b = generate_hero(heroes_df, faction_b)

    army_a = generate_army(hero_a.faction, units_df)
    army_b = generate_army(hero_b.faction, units_df)

    print("=== HERO A ===")
    print(hero_a)
    print("\n=== ARMY A ===")
    for unit in army_a.units:
        print(unit.name, unit.count, "ranged:", unit.is_ranged)

    print("\n=== HERO B ===")
    print(hero_b)
    print("\n=== ARMY B ===")
    for unit in army_b.units:
        print(unit.name, unit.count, "ranged:", unit.is_ranged)

    engine = BattleEngine(
        army_a=army_a,
        army_b=army_b,
        hero_a=hero_a,
        hero_b=hero_b
    )

    result = engine.battle()

    print("\n=== BATTLE RESULT ===")
    print(result)


if __name__ == "__main__":
    main()