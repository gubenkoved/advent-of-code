import re


file = open('data.txt', 'r')

value_map = {}
formulas = []

while True:
    line = file.readline()

    if line == '\n':
        break

    k, v = line.split(': ')
    value_map[k] = int(v)

while True:
    line = file.readline()

    if not line:
        break

    match = re.match('([a-z0-9]+) (OR|XOR|AND) ([a-z0-9]+) -> ([a-z0-9]+)', line)

    assert match is not None

    formulas.append((
        match.group(1),
        match.group(2),
        match.group(3),
        match.group(4)
    ))

formulas_map = {}

for a, op, b, r in formulas:
    assert r not in formulas_map
    formulas_map[r] = (a, op, b)


def calculate(reg):
    if reg in value_map:
        return value_map[reg]

    a, op, b = formulas_map[reg]

    if op == 'OR':
        return calculate(a) | calculate(b)
    elif op == 'XOR':
        return calculate(a) ^ calculate(b)
    elif op == 'AND':
        return calculate(a) & calculate(b)
    else:
        assert False


result = 0
for reg in formulas_map:
    val = calculate(reg)
    if reg.startswith('z'):
        bit = int(reg[1:])
        result |= val << bit
print(result)
