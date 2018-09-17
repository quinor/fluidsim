#!/usr/bin/env python3
from simulation import Simulation

s = Simulation(3, 2)

def testcase1(sim):
    sim.enable_cell(1, 0, 100)
    sim.enable_cell(0, 1, 0)
    sim.enable_cell(1, 1, 0)
    sim.enable_cell(2, 1, 0)
    sim.hor_v[0][1] = 100

def testcase2(sim):
    sim.enable_cell(1, 0, 100)
    sim.enable_cell(0, 1, 60)
    sim.enable_cell(1, 1, 0)
    sim.enable_cell(2, 1, 0)
    sim.hor_v[0][1] = 100

def testcase3(sim):
    sim.enable_cell(1, 0, 100)
    sim.enable_cell(0, 1, 100)
    sim.enable_cell(1, 1, 0)
    sim.enable_cell(2, 1, 0)
    sim.hor_v[0][1] = 100
    sim.ver_v[1][0] = 100

def testcase4(sim):
    sim.enable_cell(1, 0, 100)
    sim.enable_cell(0, 1, 20)
    sim.enable_cell(1, 1, 20)
    sim.enable_cell(2, 1, 20)
    sim.hor_v[0][1] = 100
    sim.ver_v[1][0] = 20
    sim.ver_v[1][1] = 20
    sim.ver_v[1][2] = 20
    sim.ver_v[1][3] = 20

testcase4(s)

s.update_display()

s.display.print()

while True:
    inp = input()
    if inp == 'q':
        break
    print("\r\033[1A", end="")
    s.display.clean()
    s.step()
    s.display.print()
