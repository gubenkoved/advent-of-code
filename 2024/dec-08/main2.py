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

# def dist(p1, p2):
#     return math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)

def vector(p1, p2):
    return (p2[0] - p1[0], p2[1] - p1[1])

def scale(vector, factor):
    return (vector[0] * factor, vector[1] * factor)

def length(vector):
    return math.sqrt(vector[0] ** 2 + vector[1] ** 2)

def norm(vector):
    l = length(vector)
    return (vector[0] / l, vector[1] / l)

def eq(v1, v2, precision=10**-5):
    return abs(v1[0] - v2[0]) <= precision and abs(v1[1] - v2[1]) <= precision


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

                    if (v1 == (0, 0) or v2 == (0, 0) or
                            v2 == scale(v1, 2) or
                            eq(norm(v1), norm(v2)) or
                            eq(norm(v1), scale(norm(v2), -1))):
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
