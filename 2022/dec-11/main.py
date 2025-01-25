import functools

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
    (lambda x: x % 7 == 0, 6, 2),
    (lambda x: x % 11 == 0, 5, 0),
    (lambda x: x % 13 == 0, 4, 3),
    (lambda x: x % 3 == 0, 1, 7),
    (lambda x: x % 17 == 0, 3, 7),
    (lambda x: x % 2 == 0, 0, 6),
    (lambda x: x % 5 == 0, 2, 4),
    (lambda x: x % 19 == 0, 5, 1),
]

counters = [0] * n

for _ in range(20):
    for idx in range(n):
        for x in items[idx]:
            counters[idx] += 1
            new_x = operations[idx](x)
            new_x = new_x // 3
            test_fn, true_idx, false_idx = tests[idx]
            if test_fn(new_x):
                items[true_idx].append(new_x)
            else:
                items[false_idx].append(new_x)
        items[idx] = []

counters.sort()
print(counters)
print(counters[-1] * counters[-2])
