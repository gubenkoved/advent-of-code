import operator
import os
import re
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


def print_field(positions, path):
    positions_map = defaultdict(int)
    for position in positions:
        positions_map[position] += 1
    with open(path, 'w') as f:
        for row in range(height):
            for col in range(width):
                if (col, row) not in positions_map:
                    f.write('.')
                else:
                    f.write(str(positions_map[(col, row)]))
            f.write('\n')

# debug print!
# for round_idx in range(100 + 1):
#     positions = [simulate(robot[0], robot[1], round_idx) for robot in robots]
#     os.makedirs('fields', exist_ok=True)
#     print_field(positions, f'fields/{round_idx}.txt')


quadrants_count = defaultdict(int)
positions = []
for robot in robots:
    p = simulate(robot[0], robot[1], 100)
    positions.append(p)
    q_id = quadrant_id(p)
    quadrants_count[q_id] += 1

# 220827600
print(quadrants_count)
quadrants_count.pop(None, None)
print(reduce(operator.mul, quadrants_count.values(), 1))
