import re
import heapq

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



def dist(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def merge_ranges(ranges):
    heap = []
    result = []
    for start, end in ranges:
        heapq.heappush(heap, (start, 0))
        heapq.heappush(heap, (end, 1))
    nesting = 0
    start = None
    while heap:
        x, t = heapq.heappop(heap)
        if t == 0:
            if nesting == 0:
                start = x
            nesting += 1
        elif t == 1:
            nesting -= 1
            if nesting == 0:
                result.append((start, x))
    return result


limit = 4000000


for y in range(limit + 1):
    # inclusive!
    ranges = []
    for sensor_pos, beacon_pos in data:
        beacon_dist = dist(sensor_pos, beacon_pos)
        # possible delta for target row
        d = beacon_dist - abs(sensor_pos[1] - y)
        if d >= 0:
            l = sensor_pos[0] - d
            r = sensor_pos[0] + d
            ranges.append((l, r))
    ranges = merge_ranges(ranges)
    if not any(r[0] <= 0 and r[1] >= limit for r in ranges):
        print('y=%d is not fully covered!' % y)
        print(ranges)
        break

# y = 3019123
# x = 3292963
# answer: 13171855019123
