from ..models.army import Army
import random

def calculate_morale(army: Army):

    factions = set(u.faction for u in army.units)

    if all(u.faction == "Necropolis" for u in army.units):
        return 0

    if len(factions) > 1:
        return -1

    return 1


def morale_trigger(morale: int):
    if morale > 0:
        return random.random() < 0.2
    if morale < 0:
        return random.random() < 0.1
    return False