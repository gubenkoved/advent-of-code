import collections
import math

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


antinode_positions = set()

for freq, nodes in by_freq.items():
    print('checking for "%s" frequency (%d nodes)' % (freq, len(nodes)))
    # iterate all the pairs
    for i in range(len(nodes)):
        for j in range(len(nodes)):
            # check whole field for antinodes
            for row in range(rows):
                for col in range(cols):
                    v1 = vector((row, col), nodes[i])
                    v2 = vector((row, col), nodes[j])

                    if v1 == (0, 0):
                        continue

                    if v2 == scale(v1, 2):
                        antinode_positions.add((row, col))

with open('out.txt', 'w') as f:
    for row in range(rows):
        for col in range(cols):
            if (row, col) in antinode_positions:
                f.write('#')
            else:
                f.write('.')
        f.write('\n')

print(len(antinode_positions))
