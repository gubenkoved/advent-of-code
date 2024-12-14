import operator
import os
import re
import time
from collections import defaultdict
from functools import reduce

file = open('data.txt', 'r')


robots = []

# p=99,52 v=42,38
for line in file:
    m = re.match('p=([0-9]+),([0-9]+) v=(-?[0-9]+),(-?[0-9]+)', line.strip())
    assert m
    robots.append((
        # position
        (int(m.group(1)), int(m.group(2))),
        # velocity
        (int(m.group(3)), int(m.group(4))),
    ))

width, height = 101, 103

def simulate(pos, vel, rounds):
    return (
        (pos[0] + vel[0] * rounds) % width,
        (pos[1] + vel[1] * rounds) % height,
    )


def quadrant_id(position):
    mid_w = width // 2
    mid_h = height // 2

    if position[0] == mid_w or position[1] == mid_h:
        return None

    return (
        (position[0] < mid_w),
        (position[1] < mid_h),
    )


def print_field(positions, path, label):
    positions_map = defaultdict(int)
    for position in positions:
        positions_map[position] += 1
    with open(path, 'a') as f:
        f.write(label + '\n')
        for row in range(height):
            for col in range(width):
                if (col, row) not in positions_map:
                    f.write('.')
                else:
                    f.write(str(positions_map[(col, row)]))
            f.write('\n')


# i've used intuition that number should be around W * H, then gave couple of tries
# to advent of code to determine the range!
for round_idx in range(7000, 10000):
    print('round #%d' % round_idx)
    positions = [simulate(robot[0], robot[1], round_idx) for robot in robots]
    os.makedirs('fields', exist_ok=True)
    print_field(positions, f'fields/merged.txt', f'ROUND {round_idx}')

# then just open in text editor and hold pg-down :) human eye will be able to pick it up!
