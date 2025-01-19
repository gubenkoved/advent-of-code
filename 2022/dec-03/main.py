r = []

with open('data.txt', 'r') as file:
    while True:
        line = file.readline()

        if not line:
            break

        line = line.strip()
        a, b = line[:len(line) // 2], line[len(line) // 2:]
        r.append((a, b))


# Lowercase item types a through z have priorities 1 through 26.
# Uppercase item types A through Z have priorities 27 through 52.

def priority(x: str):
    if x.islower():
        return ord(x) - ord('a') + 1
    else:
        assert x.isupper()
        return ord(x) - ord('A') + 27


total = 0
for a, b in r:
    common = set(a) & set(b)
    total += sum(priority(x) for x in common)

print(total)
