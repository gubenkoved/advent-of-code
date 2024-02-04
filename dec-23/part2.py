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


overall_longest = -1


def walk(field, cur: Tuple[int, int], visited: set) -> int:
    global overall_longest
    row, col = cur

    # finished
    if row == len(field) - 1:
        overall_longest = max(overall_longest, len(visited))
        print('path with len %5d found, longest: %5d' % (len(visited), overall_longest))

        return len(visited)

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
            inner_count = walk(field, neighbor, visited)
            longest = max(longest, inner_count)
            visited.discard(neighbor)

    return longest


def solve():
    sys.setrecursionlimit(1000000)
    field = read_field()

    print(walk(
        field,
        cur=(0, 1),
        visited=set()))


if __name__ == '__main__':
    solve()
