from src.army_generator import load_units, generate_army
from src.hero_generator import load_heroes, generate_hero
from src.engine.battle_engine import BattleEngine


UNITS_PATH = "data/raw/Heroes of Might and Magic 3 Units.csv"
HEROES_PATH = "data/raw/Heroes of Might and Magic 3 Heroes.csv"


def test_generate_army():
    units_df = load_units(UNITS_PATH)

    army = generate_army("Castle", units_df)

    assert len(army.units) >= 3
    assert len(army.units) <= 7
    assert all(unit.count > 0 for unit in army.units)


def test_generate_hero():
    heroes_df = load_heroes(HEROES_PATH)

    hero = generate_hero(heroes_df, "Castle")

    assert hero.faction == "Castle"
    assert hero.attack_skill >= 0
    assert hero.defense_skill >= 0


def test_battle_engine_runs():
    units_df = load_units(UNITS_PATH)
    heroes_df = load_heroes(HEROES_PATH)

    hero_a = generate_hero(heroes_df, "Castle")
    hero_b = generate_hero(heroes_df, "Rampart")

    army_a = generate_army(hero_a.faction, units_df)
    army_b = generate_army(hero_b.faction, units_df)

    engine = BattleEngine(
        army_a=army_a,
        army_b=army_b,
        hero_a=hero_a,
        hero_b=hero_b,
    )

    result = engine.battle()

    assert "winner" in result
    assert "rounds" in result
    assert result["winner"] in ["A", "B", "draw", "timeout"]
    assert result["rounds"] > 0