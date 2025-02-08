positions = set()

with open('data.txt', 'r') as file:
    while True:
        line = file.readline()

        if not line:
            break

        pos = tuple(int(x) for x in line.split(','))
        positions.add(pos)


sides = 0
for p in positions:
    x, y, z = p
    neighbors = [
        (x + 1, y, z),
        (x - 1, y, z),
        (x, y + 1, z),
        (x, y - 1, z),
        (x, y, z + 1),
        (x, y, z - 1),
    ]
    for np in neighbors:
        if not np in positions:
            sides += 1
print(sides)
