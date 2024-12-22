import math
import functools
import sys
import heapq
from pprint import pprint

sys.setrecursionlimit(10**9)

file = open('data.txt', 'r')

codes = []
for line in file:
    codes.append(line.strip())


keypad1 = (
    '789',
    '456',
    '123',
    '.0A',
)
keypad1_start = (3, 2)

keypad2 = (
    '.^A',
    '<v>',
)
keypad2_start = (0, 2)


def position_of(keypad, char):
    for row in range(len(keypad)):
        for col in range(len(keypad[row])):
            if keypad[row][col] == char:
                return (row, col)
    return None


# returns ALL arrow paths from start to end on a given keypad
@functools.lru_cache(maxsize=None)
def paths2(keypad, start, end):
    return list(paths(keypad, start, end))

def paths(keypad, start, end):
    if start == end:
        yield ''
    r, c = start
    tr, tc = end
    dist = abs(tr - r) + abs(tc - c)
    neighbors = [
        (r - 1, c, '^'),
        (r + 1, c, 'v'),
        (r, c - 1, '<'),
        (r, c + 1, '>'),
    ]
    for nr, nc, nd in neighbors:
        if nr < 0 or nr >= len(keypad):
            continue
        if nc < 0 or nc >= len(keypad[nr]):
            continue
        ndist = abs(tr - nr) + abs(tc - nc)
        if ndist >= dist:
            continue
        if keypad[nr][nc] == '.':
            continue
        for inner in paths(keypad, (nr, nc), end):
            yield nd + inner


# returns ALL encoding of a given code on a given keypad
def encodings(keypad, code, position):
    if not code:
        yield ''
        return

    next_chr = code[0]
    next_pos = position_of(keypad, next_chr)

    for path in paths2(keypad, position, next_pos):
        for inner in encodings(keypad, code[1:], next_pos):
            yield path + 'A' + inner


def complexity(code, encoded):
    return len(encoded) * int(code[:3])

