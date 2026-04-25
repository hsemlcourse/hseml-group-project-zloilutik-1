import random
import pandas as pd
from typing import List
from src.battle_engine import Unit, Army


# =========================
# LOAD DATA
# =========================

def load_units(path: str) -> pd.DataFrame:
    df = pd.read_csv(
        path,
        sep=';',          
        engine='python'
    )

    df.columns = df.columns.str.strip().str.lower() 

    return df


# =========================
# GENERATE ARMY
# =========================

def generate_army(hero_faction: str, units_df: pd.DataFrame) -> Army:

    hero_faction = hero_faction.lower()

    faction_units = units_df[
        units_df["castle"].str.lower() == hero_faction
    ].copy()

    if faction_units.empty:
        raise ValueError(f"No units found for faction: {hero_faction}")

    num_stacks = random.randint(3, min(7, len(faction_units)))

    chosen_units = faction_units.sample(n=num_stacks, replace=False)

    weeks = random.randint(1, 6)

    army_units: List[Unit] = []

    for _, row in chosen_units.iterrows():

        growth = row["growth"]
        count = int(growth * weeks)

        unit = Unit(
            name=row["unit_name"],
            faction=row["castle"],
            speed=row["speed"],
            attack=row["attack"],
            defense=row["defence"],
            hp=row["health"],
            count=count
        )

        army_units.append(unit)

    return Army(units=army_units)


# =========================
# MAIN (TEST RUN)
# =========================

if __name__ == "__main__":

    units = load_units(
        "data/raw/Heroes of Might and Magic 3 Units.csv"
    )

    factions = units["castle"].dropna().unique().tolist()

    hero_faction = random.choice(factions)

    print("\nSELECTED FACTION:", hero_faction, "\n")

    army = generate_army(hero_faction, units)

    for u in army.units:
        print(u.name, u.count)  