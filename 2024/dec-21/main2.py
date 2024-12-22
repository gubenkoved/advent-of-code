import functools


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


# returns ALL encodings of a given code on a given keypad as tuple of atoms
# where atom is an "arrow path" starting at some position which ends with "A" to
# finally enter the character on a keypad;
# note that amount of atoms will be equal to the len of the code (by definition);
def encodings(keypad, code, position) -> tuple[str, ...]:
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


# bel stands for "best encoded len"
@functools.lru_cache(maxsize=None)
def bel(atom: str, level: int) -> int:
    assert atom[-1] == 'A'
    if level == 0:
        return len(atom)
    best_len = float('inf')
    for inner_atoms in encodings(keypad2, atom, keypad2_start):
        best_len = min(best_len, sum(
            bel(inner_atom, level - 1)
            for inner_atom in inner_atoms
        ))
    return best_len


def solve2(atoms) -> int:
    return sum(
        bel(atom, 25)
        for atom in atoms
    )


def solve(code) -> int:
    return min(
        solve2(atoms)
        for atoms in l1_encodings(code)
    )


# show all possible atoms
# possible_atoms = set()
# for c1 in '<^>vA':
#     for c2 in '<^>vA':
#         if c1 == c2:
#             continue
#         for atom in paths2(keypad2, position_of(keypad2, c1), position_of(keypad2, c2)):
#             possible_atoms.add(atom)
# print('all possible atoms: %s (%d)' % (possible_atoms, len(possible_atoms)))


result = 0
for code in codes:
    print('handling code:', code)
    encoded_len = solve(code)
    c = complexity(code, encoded_len)
    print('  best encoded len: %d, complexity: %d' % (encoded_len, c))
    result += c
print(result)
