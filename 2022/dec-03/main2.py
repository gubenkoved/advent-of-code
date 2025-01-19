from functools import reduce

r = []

with open('data.txt', 'r') as file:
    while True:
        line = file.readline()

        if not line:
            break

        line = line.strip()
        r.append(line)


# Lowercase item types a through z have priorities 1 through 26.
# Uppercase item types A through Z have priorities 27 through 52.

def priority(x: str):
    if x.islower():
        return ord(x) - ord('a') + 1
    else:
        assert x.isupper()
        return ord(x) - ord('A') + 27

result = 0
for idx in range(0, len(r), 3):
    r3 = r[idx:idx + 3]
    sets = [set(rc) for rc in r3]
    common = reduce(set.intersection, sets)
    assert len(common) == 1
    result += priority(next(iter(common)))

print(result)
