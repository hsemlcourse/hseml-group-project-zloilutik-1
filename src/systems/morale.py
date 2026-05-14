from ..models.army import Army
import random


def calculate_morale(army: Army) -> int:
    factions = {u.faction for u in army.units}

    if all(u.faction == "Necropolis" for u in army.units):
        return 0

    if len(factions) > 1:
        return -1

    return 1


def morale_event(morale: int) -> str:
    """
    Returns:
    - "extra" for good morale extra action
    - "skip" for bad morale skipped action
    - "none" if nothing happens
    """
    if morale > 0:
        return "extra" if random.random() < 0.2 else "none"

    if morale < 0:
        return "skip" if random.random() < 0.1 else "none"

    return "none"