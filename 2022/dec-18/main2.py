positions = set()

with open('data.txt', 'r') as file:
    while True:
        line = file.readline()

        if not line:
            break

        pos = tuple(int(x) for x in line.split(','))
        positions.add(pos)



def neighbors(x, y, z):
    return [
        (x + 1, y, z),
        (x - 1, y, z),
        (x, y + 1, z),
        (x, y - 1, z),
        (x, y, z + 1),
        (x, y, z - 1),
    ]


# find exterior cubes and only count sides that are neighboring with them
# only consider a cube which is just a 1 unit bigger in all dimensions
exterior = set()

maxs = []
mins = []
for dim in range(3):
    maxs.append(max(p[dim] for p in positions))
    mins.append(min(p[dim] for p in positions))


stack = [(mins[0] - 1, mins[1] - 1, mins[2] - 1)]
while stack:
    p = stack.pop(-1)
    if p in exterior:
        continue
    exterior.add(p)
    for np in neighbors(*p):
        # limit the traversal
        too_far = False
        for dim in range(3):
            if (np[dim] < mins[dim] - 1) or (np[dim] > maxs[dim] + 1):
                too_far = True
                break

        # outside of bounding cube
        if too_far:
            continue

        # can not go where lava is
        if np in positions:
            continue

        if np not in exterior:
            stack.append(np)


sides = 0
for p in positions:
    for np in neighbors(*p):
        if not np in positions and np in exterior:
            sides += 1
print(sides)
