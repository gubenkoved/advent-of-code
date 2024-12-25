file = open('data.txt', 'r')

keys = []
locks = []


while True:
    block = []

    while True:
        line = file.readline()
        if not line or line == '\n':
            break
        block.append(line.strip())

    if not block:
        break

    # handle block
    if block[0][0] == '#':
        # read lock
        lock = []
        for col in range(len(block[0])):
            h = 0
            for row in range(len(block)):
                if block[row][col] != '#':
                    break
                h += 1
            lock.append(h)
        locks.append(lock)
    else:
        key = []
        for col in range(len(block[0])):
            h = 0
            for row in range(len(block) - 1, -1, -1):
                if block[row][col] != '#':
                    break
                h += 1
            key.append(h)
        keys.append(key)


def fits(lock, key):
    return all(a + b <= 7 for a, b in zip(lock, key))


result = 0
for lock in locks:
    for key in keys:
        if fits(lock, key):
            result += 1
print(result)
