import functools
import sys
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
    assert code, 'no code'
    next_chr = code[0]
    next_pos = position_of(keypad, next_chr)

    for path in paths2(keypad, position, next_pos):
        if len(code) > 1:
            for inner in encodings(keypad, code[1:], next_pos):
                yield (path + 'A',) + inner
        else:
            yield (path + 'A',)


def complexity(code, encoded_len):
    return encoded_len * int(code[:3])


# returns possible paths on the first (L1) keypad for a given code
def l1_encodings(code):
    return list(encodings(keypad1, code, keypad1_start))


# example: ^^>A -> best len on given encoding level
@functools.lru_cache(maxsize=None)
def encode(atom, level) -> int:
    assert atom[-1] == 'A'
    if level == 0:
        return len(atom)
    best_len = float('inf')
    for inner in encodings(keypad2, atom, keypad2_start):
        inner_total_len = 0
        for inner_atom in inner:
            inner_total_len += encode(inner_atom, level - 1)
        if inner_total_len < best_len:
            best_len = inner_total_len
    return best_len


def solve2(atoms) -> int:
    return sum(
        encode(atom, 25)
        for atom in atoms
    )


def solve(code) -> int:
    return min(
        solve2(atoms)
        for atoms in l1_encodings(code)
    )


result = 0
for code in codes:
    print('handling code:', code)
    encoded_len = solve(code)
    c = complexity(code, encoded_len)
    print('  encoded len: %d, complexity: %d' % (encoded_len, c))
    result += c
print(result)
