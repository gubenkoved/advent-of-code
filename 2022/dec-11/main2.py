import copy

n = 8

items = [
    [63, 57],
    [82, 66, 87, 78, 77, 92, 83],
    [97, 53, 53, 85, 58, 54],
    [50],
    [64, 69, 52, 65, 73],
    [57, 91, 65],
    [67, 91, 84, 78, 60, 69, 99, 83],
    [58, 78, 69, 65],
]

operations = [
    lambda x: x * 11,
    lambda x: x + 1,
    lambda x: x * 7,
    lambda x: x + 3,
    lambda x: x + 6,
    lambda x: x + 5,
    lambda x: x * x,
    lambda x: x + 7,
]

tests = [
    # (reminder, if true, if false)
    (7, 6, 2),
    (11, 5, 0),
    (13, 4, 3),
    (3, 1, 7),
    (17, 3, 7),
    (2, 0, 6),
    (5, 2, 4),
    (19, 5, 1),
]

counters = [0] * n

# dict reminder -> items
items2 = {}

# replace items with its reminders
for rem, _, _ in tests:
    items2[rem] = copy.deepcopy(items)
    for lst in items2[rem]:
        mapped = [x % rem for x in lst]
        lst.clear()
        lst.extend(mapped)

del items

# moves element "el_idx" from specific monkey to another one for all the
# reminders inside items2
def move(from_idx, el_idx, to_idx):
    for rem in items2:
        elem = items2[rem][from_idx].pop(el_idx)
        items2[rem][to_idx].append(elem)

# now at each step when processing item process it inside all the items2 collection
# meaning for each reminder
# this is based on the fact that:
# x * A mod K = ((x mod K) * A) mod K
# x * x mod K = (x mod K) * (x mod K) mod K
# meaning on each step we can just replace x with (x mod K) to trim the number
for round_idx in range(10000):
    print('processing round %d' % round_idx)
    for idx in range(n):
        op_fn = operations[idx]
        # compute the result of the operation modulus all the needed ones
        for rem in items2:
            new_items = []
            for x in items2[rem][idx]:
                new_x = op_fn(x) % rem
                new_items.append(new_x)
            items2[rem][idx] = new_items

        # now we move things around using the rule for the given monkey
        target_rem, true_idx, false_idx = tests[idx]
        for el_idx in range(len(items2[target_rem][idx]) - 1, -1, -1):
            counters[idx] += 1
            if items2[target_rem][idx][el_idx] == 0:
                move(idx, el_idx, true_idx)
            else:
                move(idx, el_idx, false_idx)

counters.sort()
print(counters)
print(counters[-1] * counters[-2])
