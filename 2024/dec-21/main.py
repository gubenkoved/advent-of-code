from dataclasses import field

file = open('data.txt', 'r')

codes = []
for line in file:
    codes.append(line.strip())


keypad1 = [
    '789',
    '456',
    '123',
    '.0A',
]
keypad1_start = (3, 2)

keypad2 = [
    '.^A',
    '<v>',
]
keypad2_start = (0, 2)


def position_of(keypad, char):
    for row in range(len(keypad)):
        for col in range(len(keypad[row])):
            if keypad[row][col] == char:
                return (row, col)
    return None


# returns sequence of arrows from the start to the end coordinates on the keypad
def find_path(keypad, start, end):
    rows, cols = len(keypad), len(keypad[0])
    queue = [(start, '')]
    visited = set()
    while queue:
        (r, c), seq = queue.pop(0)
        if (r, c) in visited:
            continue
        visited.add((r, c))
        if (r, c) == end:
            return seq
        neighbors = [
            (r - 1, c, '^'),
            (r + 1, c, 'v'),
            (r, c - 1, '<'),
            (r, c + 1, '>'),
        ]
        for nr, nc, nchr in neighbors:
            if nr < 0 or nr >= rows:
                continue
            if nc < 0 or nc >= cols:
                continue
            queue.append(((nr, nc), seq + nchr))
    assert False, 'no path'


# should calculate the movement for the first level of the keypad
def encode(keypad, code, pos):
    if not code:
        return ''

    target_chr = code[0]
    target_pos = position_of(keypad, target_chr)

    arrows = find_path(keypad, pos, target_pos)
    return ''.join(arrows) + 'A' + encode(keypad, code[1:], target_pos)


def triple_encode(code):
    s1 = encode(keypad1, code, keypad1_start)
    s2 = encode(keypad2, s1, keypad2_start)
    s3 = encode(keypad2, s2, keypad2_start)
    return s3


def complexity(code, encoded):
    return len(encoded) * int(code[:3])

result = 0
for code in codes:
    encoded = triple_encode(code)
    c = complexity(code, encoded)
    print('%s: %s (%d)' % (code, encoded, c))
    result += c
print(result)
