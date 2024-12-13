import re
import math

file = open('data.txt', 'r')

data = []

re1 = 'Button .: X\+([0-9]+), Y\+([0-9]+)'
re2 = 'Prize: X=([0-9]+), Y=([0-9]+)'

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
        (int(m3.group(1)), int(m3.group(2))),
    ))

    fin = file.readline()

    if not fin:
        break


def solve(b1, b2, r):
    min_price = math.inf
    for c1 in range(101):
        for c2 in range(101):
            price = 3 * c1 + c2
            if (c1 * b1[0] + c2 * b2[0] == r[0] and
                    c1 * b1[1] + c2 * b2[1] == r[1]):
                min_price = min(min_price, price)
    return min_price

result = 0
for b1, b2, r in data:
    price = solve(b1, b2, r)
    if price != math.inf:
        result += price
print(result)
