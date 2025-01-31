import re

data = []

with open('data.txt', 'r') as file:
    while True:
        line = file.readline()

        if not line:
            break

        match = re.match(
            'Sensor at x=([0-9]+), y=([0-9]+): closest beacon is at x=(-?[0-9]+), y=(-?[0-9]+)', line.strip())

        assert match

        data.append((
            # sensor pos
            (int(match.group(1)), int(match.group(2))),
            # closest beacon position
            (int(match.group(3)), int(match.group(4))),
        ))

# each sensor basically draws rhombus on the field, and we need to count
# filled pixels on a given row

target_y = 2000000

# x coordinates only
shadow = set()


def dist(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


for sensor_pos, beacon_pos in data:
    # find all the points it shadows on target_y row
    beacon_dist = dist(sensor_pos, beacon_pos)

    # possible delta for target row
    d = beacon_dist - abs(sensor_pos[1] - target_y)
    for cur_d in range(d + 1):
        shadow.add(sensor_pos[0] - cur_d)
        shadow.add(sensor_pos[0] + cur_d)

# drop the beacon position though
for _, beacon_pos in data:
    if beacon_pos[1] == target_y:
        shadow.discard(beacon_pos[0])

print(len(shadow))
