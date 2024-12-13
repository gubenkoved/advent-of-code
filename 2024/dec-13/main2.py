import re
from fractions import Fraction

file = open('data.txt', 'r')

data = []

re1 = 'Button .: X\+([0-9]+), Y\+([0-9]+)'
re2 = 'Prize: X=([0-9]+), Y=([0-9]+)'

const = 10000000000000

while True:
    line1 = file.readline().strip()
    line2 = file.readline().strip()
    line3 = file.readline().strip()

    m1 = re.match(re1, line1)
    m2 = re.match(re1, line2)
    m3 = re.match(re2, line3)

    assert m1
    assert m2
    assert m3

    data.append((
        # first button
        (int(m1.group(1)), int(m1.group(2))),
         # second button
        (int(m2.group(1)), int(m2.group(2))),
        # result
        # (int(m3.group(1)), int(m3.group(2))),
        (int(m3.group(1)) + const, int(m3.group(2)) + const),
    ))

    fin = file.readline()

    if not fin:
        break


def solve(b1, b2, r):
    # this is system of equations
    # we have 2 unknowns c1 and c2 and two equations
    # c1 * b1[0] + c2 * b2[0] = r[0]
    # c1 * b1[1] + c2 * b2[1] = r[1]

    # let's change coefficients in a way that makes it possible to
    # subtract one from another and eliminate one -- we need to multiply
    # the second one on b1[0]/b1[1], then we have:
    #
    # c1 * b1[0] + c2 * b2[0] = r[0]
    # c1 * b1[0] + c2 * b1[0] * b2[1] / b1[1] = r[1] * b1[0] / b1[1]

    # subtract second from first
    # c2 * (b2[0] - b1[0] * b2[1] / b1[1]) = r[0] - r[1] * b1[0] / b1[1]
    # then we have c2, and then we have c1 as
    # c1 = (r[0] - c2 * b2[0]) / b1[0]

    k = Fraction(b1[0], b1[1])
    c2 = (r[0] - r[1] * k) / (b2[0] - b2[1] * k)
    c1 = (r[0] - c2 * b2[0]) / b1[0]

    if c1.numerator % c1.denominator != 0:
        return None

    if c2.numerator % c2.denominator != 0:
        return None

    return int(3 * c1 + c2)

result = 0
for b1, b2, r in data:
    price = solve(b1, b2, r)
    print(price)
    if price != None:
        result += price

print('***')
print(result)
