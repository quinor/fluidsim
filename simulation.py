from display import Display
import copy
import math


def mycopysign(x, val):
    if abs(val) < 1e-3:
        return 0
    return math.copysign(x, val)


class Simulation:

    def flow(self, old, pressure):
        return old*0.9 + mycopysign(5, pressure)

    def __init__(self, w, h):
        self.size = (w, h)
        self.display = Display(w, h)

        self.enabled = [[False for _ in range(w)] for _ in range(h)]
        self.amount = [[0 for _ in range(w)] for _ in range(h)]

        self.hor_v = [[0 for __ in range(w)] for _ in range(h+1)]
        self.ver_v = [[0 for __ in range(w+1)] for _ in range(h)]
        self.hor_f = [[0 for __ in range(w)] for _ in range(h+1)]
        self.ver_f = [[0 for __ in range(w+1)] for _ in range(h)]

    def enable_cell(self, x, y, amt):
        assert 0 <= y < self.size[1]
        assert 0 <= x < self.size[0]
        self.enabled[y][x] = True
        self.amount[y][x] = amt

    def step(self):
        w, h = self.size

        for y in range(h-1):
            for x in range(w):
                if self.enabled[y][x] and self.enabled[y+1][x]:
                    self.hor_v[y+1][x] = self.flow(
                        self.hor_v[y+1][x],
                        self.amount[y][x] - self.amount[y+1][x]
                    )
        for y in range(h):
            for x in range(w-1):
                if self.enabled[y][x] and self.enabled[y][x+1]:
                    self.ver_v[y][x+1] = self.flow(
                        self.ver_v[y][x+1],
                        self.amount[y][x] - self.amount[y][x+1]
                    )

        self.ver_f = copy.deepcopy(self.ver_v)
        self.hor_f = copy.deepcopy(self.hor_v)

        for y in range(h):
            for x in range(w):
                if self.enabled[y][x]:
                    vin = 0
                    vout = 0
                    vin += max(0, self.hor_v[y][x]) + max(0, -self.hor_v[y+1][x],)
                    vout += max(0, -self.hor_v[y][x]) + max(0, self.hor_v[y+1][x],)
                    vin += max(0, self.ver_v[y][x]) + max(0, -self.ver_v[y][x+1],)
                    vout += max(0, -self.ver_v[y][x]) + max(0, self.ver_v[y][x+1],)
                    amt = self.amount[y][x]
                    sat_in = 1 if abs(vin-0) < 1e-9 else min(vin, 100-amt)/vin
                    sat_out = 1 if abs(vout-0) < 1e-9 else min(vout, amt)/vout

                    self.hor_f[y][x] = \
                        min(self.hor_f[y][x], self.hor_v[y][x]*sat_in) \
                        if self.hor_v[y][x] > 0 else \
                        max(self.hor_f[y][x], self.hor_v[y][x]*sat_out)

                    self.hor_f[y+1][x] = \
                        min(self.hor_f[y+1][x], self.hor_v[y+1][x]*sat_out) \
                        if self.hor_v[y+1][x] > 0 else \
                        max(self.hor_f[y+1][x], self.hor_v[y+1][x]*sat_in)

                    self.ver_f[y][x] = \
                        min(self.ver_f[y][x], self.ver_v[y][x]*sat_in) \
                        if self.ver_v[y][x] > 0 else \
                        max(self.ver_f[y][x], self.ver_v[y][x]*sat_out)

                    self.ver_f[y][x+1] = \
                        min(self.ver_f[y][x+1], self.ver_v[y][x+1]*sat_out) \
                        if self.ver_v[y][x+1] > 0 else \
                        max(self.ver_f[y][x+1], self.ver_v[y][x+1]*sat_in)

        self.update_display()

        for y in range(1, h):
            for x in range(w):
                self.hor_v[y][x] = self.hor_f[y][x]

        for y in range(h):
            for x in range(1, w):
                self.ver_v[y][x] = self.ver_f[y][x]

        for y in range(h):
            for x in range(w):
                self.amount[y][x] += \
                    self.hor_f[y][x] - self.hor_f[y+1][x] + \
                    self.ver_f[y][x] - self.ver_f[y][x+1]

    def update_display(self):
        w, h = self.size

        for i in range(h):
            for j in range(w):
                if self.enabled[i][j]:
                    self.display.blocks[i][j].set(self.amount[i][j])
        for i in range(h):
            for j in range(w+1):
                self.display.verticals[i][j].set(self.ver_f[i][j])

        for i in range(h+1):
            for j in range(w):
                self.display.horizontals[i][j].set(self.hor_f[i][j])
