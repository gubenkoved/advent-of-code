from typing import Tuple
import sys


sys.setrecursionlimit(1000000)


field = []

with open('data.txt', 'r') as f:
    while True:
        line = f.readline()
        if not line:
            break
        field.append(line.strip())

rows, cols = len(field), len(field[0])
overall_longest = 0


def walk(cur: Tuple[int, int], constraint: str, visited: set) -> int:
    global overall_longest

    row, col = cur

    # finished
    if row == len(field) - 1:
        overall_longest = max(overall_longest, len(visited))
        print('path with len %5d found, longest so far: %5d steps' % (len(visited), overall_longest))
        return len(visited)

    if constraint == '>':
        neighbors = [
            (row, col + 1),
        ]
    elif constraint == '<':
        neighbors = [
            (row, col - 1),
        ]
    elif constraint == 'v':
        neighbors = [
            (row + 1, col),
        ]
    elif constraint == '^':
        neighbors = [
            (row - 1, col),
        ]
    else:  # not constrained
        neighbors = [
            (row + 1, col),
            (row - 1, col),
            (row, col - 1),
            (row, col + 1),
        ]

    longest = -1

    for neighbor in neighbors:
        if neighbor[0] < 0 or neighbor[0] >= rows:
            continue
        if neighbor[1] < 0 or neighbor[1] >= cols:
            continue
        if field[neighbor[0]][neighbor[1]] == '#':
            continue
        if neighbor not in visited:
            visited.add(neighbor)
            neighbor_char = field[neighbor[0]][neighbor[1]]
            inner_count = walk(neighbor, neighbor_char, visited)
            longest = max(longest, inner_count)
            visited.discard(neighbor)

    return longest


print(walk(
    cur=(0, 1),
    constraint='',
    visited=set()))
