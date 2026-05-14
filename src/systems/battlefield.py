class BattleField:

    def __init__(self):
        self.h = 11
        self.w = 15

    def get_positions(self, n, side):
        positions = []

        if n <= 0:
            return positions

        step = self.h // (n + 1)

        for i in range(n):
            y = (i + 1) * step
            x = 1 if side == "A" else self.w - 2
            positions.append((x, y))

        return positions

    def place_army(self, army, side):
        positions = self.get_positions(len(army.units), side)

        for unit, (x, y) in zip(army.units, positions):
            unit.x = x
            unit.y = y

    def distance(self, unit_a, unit_b):
        return abs(unit_a.x - unit_b.x) + abs(unit_a.y - unit_b.y)