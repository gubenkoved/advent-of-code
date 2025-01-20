ranges = []

with open('data.txt', 'r') as file:
    while True:
        line = file.readline()

        if not line:
            break

        a, b = line.split(',')

        ranges.append((
            tuple(int(x) for x in a.split('-')),
            tuple(int(x) for x in b.split('-')),
        ))


# returns True if r1 fully contains r2
def contains(r1, r2):
    return r1[0] <= r2[0] and r1[1] >= r2[1]


def overlaps(r1, r2):
    if r1[0] > r2[0]:
        return overlaps(r2, r1)

    return r2[0] <= r1[1]


# contains
result = 0
for r1, r2 in ranges:
    if contains(r1, r2) or contains(r2, r1):
        result += 1

print(result)

# overlap
print(sum(1 for r1, r2 in ranges if overlaps(r1, r2)))
