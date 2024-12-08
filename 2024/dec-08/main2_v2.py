import collections
import math
from fractions import Fraction

file = open('data.txt', 'r')
field = [line.strip() for line in file.readlines()]

rows, cols = len(field), len(field[0])

by_freq = collections.defaultdict(list)

for row in range(rows):
    for col in range(cols):
        if field[row][col] == '.':
            continue
        by_freq[field[row][col]].append((row, col))

def vector(p1, p2):
    return p2[0] - p1[0] + (p2[1] - p1[1])*1j

def norm(x):
    l = abs(x)
    return x / l

def eq(x1, x2):
    return abs(x1 - x2) < (10 ** -5)

antinode_positions = set()

for freq, nodes in by_freq.items():
    print('checking for "%s" frequency (%d nodes)' % (freq, len(nodes)))
    # iterate all the pairs
    for i in range(len(nodes)):
        for j in range(len(nodes)):
            if i == j:
                continue
            # check whole field for antinodes
            for row in range(rows):
                for col in range(cols):
                    v1 = vector((row, col), nodes[i])
                    v2 = vector((row, col), nodes[j])

                    if (eq(v1, 0) or
                            eq(v2, 0) or
                            eq(v2, 2 * v1) or
                            eq(norm(v1), norm(v2)) or
                            eq(norm(v1), -1 * norm(v2))):
                        antinode_positions.add((row, col))

with open('out2.txt', 'w') as f:
    for row in range(rows):
        for col in range(cols):
            if (row, col) in antinode_positions:
                f.write('#')
            else:
                f.write('.')
        f.write('\n')

print(len(antinode_positions))
