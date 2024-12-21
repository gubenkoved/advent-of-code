import math
import functools
import sys

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


# returns sequence of arrows from the start to the end coordinates on the keypad
@functools.lru_cache()
def all_paths(keypad, start, end):
    sr, sc = start
    tr, tc = end
    r, c = start
    cur_dist = abs(tr - sr) + abs(tc - sc)
    neighbors = [
        (r - 1, c, '^'),
        (r + 1, c, 'v'),
        (r, c - 1, '<'),
        (r, c + 1, '>'),
    ]
    paths = []
    for nr, nc, nchr in neighbors:
        if nr < 0 or nr >= len(keypad):
            continue
        if nc < 0 or nc >= len(keypad[nr]):
            continue
        # do not point at gaps!
        if keypad[nr][nc] == '.':
            continue
        # if we are not approaching the target, skip
        n_dist = abs(tr - nr) + abs(tc - nc)
        if n_dist >= cur_dist:
            continue
        if n_dist == 0:
            paths.append(nchr)
        else:
            for inner_path in all_paths(keypad, (nr, nc), end):
                paths.append(nchr + inner_path)
    return paths


def encodings(keypad, code, pos):
    if not code:
        yield ''
        return

    target_chr = code[0]
    target_pos = position_of(keypad, target_chr)

    if pos != target_pos:
        for arrows in all_paths(keypad, pos, target_pos):
            for inner_result in encodings(keypad, code[1:], target_pos):
                yield ''.join(arrows) + 'A' + inner_result
    else:
        for inner_result in encodings(keypad, code[1:], target_pos):
            yield 'A' + inner_result


def encodings_level(code, level):
    if level == 0:
        # final one (real keypad)
        yield from encodings(keypad1, code, keypad1_start)
    else:
        for inner_code in encodings_level(code, level - 1):
            yield from encodings(keypad2, inner_code, keypad2_start)


def complexity(code, encoded):
    return len(encoded) * int(code[:3])


result = 0
for code in codes:
    print('handling code {}'.format(code))
    min_complexity = math.inf
    min_encoding = None
    for encoding in encodings_level(code, 25 + 1):
        c = complexity(code, encoding)
        if c < min_complexity:
            min_complexity = c
            min_encoding = encoding
            print('** %s: %s (%d)' % (code, min_encoding, min_complexity))
    print('%s: %s (%d)' % (code, min_encoding, min_complexity))
    result += min_complexity
print('result: %s' % result)
