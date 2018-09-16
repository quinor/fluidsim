

class PrintBlock:

    def __init__(self, init_blk):
        self.block = init_blk[:]
        h = len(self.block)
        assert h > 0
        ls = [len(e) for e in self.block]
        assert min(ls) == max(ls)
        w = ls[0]
        self.size = (w, h)

    def println(self, no):
        assert 0 <= no < self.size[1]
        print(self.block[no], end="")

class Horizontal(PrintBlock):
    def __init__(self):
        super().__init__(["     ", "-----", "     "])

    def set(self, flow): # positive down, negative up, zero none
        if flow == 0.:
            self.block = ["     ", "-----", "     "]
        elif flow < 0:
            self.block = ["^^^^^", "{:.1f}".format(-flow).center(5), "^^^^^"]
        elif flow > 0:
            self.block = ["vvvvv", "{:.1f}".format(flow).center(5), "vvvvv"]
        else:
            assert False

class Vertical(PrintBlock):
    def __init__(self):
        super().__init__(["   |   ", "   |   ", "   |   "])

    def set(self, flow): # positive right, negative left, zero none
        if flow == 0.:
            self.block = ["   |   ", "   |   ", "   |   "]
        elif flow < 0:
            self.block = ["  <<<  ", " "+"{:.1f}".format(-flow).center(5)+" ", "  <<<  "]
        elif flow > 0:
            self.block = ["  >>>  ", " "+"{:.1f}".format(flow).center(5)+" ", "  >>>  "]
        else:
            assert False


class Block(PrintBlock):
    def __init__(self):
        super().__init__(["     ", "     ", "     "])

    def set(self, amount): # positive right, negative left, zero none
        self.block[1] = "{:.1f}".format(amount).center(5)


class Display:
    plus = PrintBlock(["   |   ", "---+---", "   |   "])

    def __init__(self, w, h):
        self.verticals = [[Vertical() for __ in range(w+1)] for _ in range(h)]
        self.horizontals = [[Horizontal() for __ in range(w)] for _ in range(h+1)]
        self.blocks = [[Block() for __ in range(w)] for _ in range(h)]
        self.size = (w, h)

    def _print_edge(self, i):
        for j in range(3):
            self.plus.println(j)
            for h in self.horizontals[i]:
                h.println(j)
                self.plus.println(j)
            print("")

    def _print_middle(self, i):
        for j in range(3):
            for v, b in zip(self.verticals[i], self.blocks[i]):
                v.println(j)
                b.println(j)
            self.verticals[i][-1].println(j)
            print("")

    def print (self):
        for i in range(self.size[1]):
            self._print_edge(i)
            self._print_middle(i)
        self._print_edge(self.size[1])

    def clean (self):
        wl = self.size[0] * 12 + 7
        hl = self.size[1] * 6 + 3
        print("\r\033[{}A".format(hl), end="")
