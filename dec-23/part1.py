from typing import Tuple
import sys


def read_field():
    field = []

    with open('data.txt', 'r') as f:
        while True:
            line = f.readline()
            if not line:
                break
            field.append(line.strip())
    return field


def walk(field, cur: Tuple[int, int], constraint: str, visited: set, on_step_fn=None) -> int:
    row, col = cur

    if on_step_fn:
        on_step_fn(cur, visited)

    # finished
    if row == len(field) - 1:
        print('path with len %5d found' % len(visited))
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
        if neighbor[0] < 0 or neighbor[0] >= len(field):
            continue
        if neighbor[1] < 0 or neighbor[1] >= len(field[0]):
            continue
        if field[neighbor[0]][neighbor[1]] == '#':
            continue
        if neighbor not in visited:
            visited.add(neighbor)
            neighbor_char = field[neighbor[0]][neighbor[1]]
            inner_count = walk(field, neighbor, neighbor_char, visited, on_step_fn)
            longest = max(longest, inner_count)
            visited.discard(neighbor)

    return longest


def solve():
    sys.setrecursionlimit(1000000)
    field = read_field()

    print(walk(
        field,
        cur=(0, 1),
        constraint='',
        visited=set()))


if __name__ == '__main__':
    solve()
