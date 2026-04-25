class BattleField:

    def __init__(self):
        self.h = 11
        self.w = 15

    def get_positions(self, n, side):
        positions = []
        step = self.h // (n + 1)

        for i in range(n):
            y = (i + 1) * step
            x = 2 if side == "A" else self.w - 3
            positions.append((x, y))

        return positions