pairs = []

with open('data.txt', 'r') as file:
    while True:
        a = file.readline()
        b = file.readline()

        pairs.append((eval(a), eval(b)))

        c = file.readline()

        if not c:
            break


# returns -1 if a is smaller than b, 0 if equal and 1 if bigger
def compare(a, b):
    if isinstance(a, int) and isinstance(b, int):
        if a == b:
            return 0
        return -1 if a < b else +1

    # make sure both are lists
    if not isinstance(a, list):
        a = [a]

    if not isinstance(b, list):
        b = [b]

    # compare lists element by element
    for x, y in zip(a, b):
        cmp = compare(x, y)
        if cmp == -1:
            return -1
        elif cmp == 0:
            # continue
            pass
        else:
            assert cmp == 1
            return 1

    # all items are the same or we exhausted one sequence first
    if len(a) == len(b):
        return 0
    elif len(a) < len(b):
        return -1
    else:
        return +1


result = 0
for idx, (a, b) in enumerate(pairs, 1):
    if compare(a, b) in (-1, 0):
        result += idx
        print('#%d is correct' % idx)
print(result)
