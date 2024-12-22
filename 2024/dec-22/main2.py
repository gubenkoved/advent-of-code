file = open('data.txt', 'r')

seeds = [int(x) for x in file]
print('seed count:', len(seeds))


def mix(a, b):
    return a ^ b

def prune(a):
    return a % 16777216

def step(x):
    x = prune(mix(x, x * 64))
    x = prune(mix(x, x // 32))
    x = prune(mix(x, x * 2048))
    return x

def price(x):
    return x % 10

def accumulate(x, step_count, window_size):
    result_map = {}  # window numbers -> max price
    p = price(x)
    window = tuple()
    for _ in range(step_count):
        x = step(x)
        p2 = price(x)
        d = p2 - p
        p = p2
        window = window + (d,)
        if len(window) > window_size:
            window = window[-window_size:]
        if len(window) == window_size:
            # only capture the first value!
            if window not in result_map:
                result_map[window] = p2
    return result_map


agg = [
    accumulate(x, 2000, 4)
    for x in seeds
]

# compute all possible windows
all_windows = set()
for window_map in agg:
    all_windows.update(window_map.keys())

best_window = None
best_profit = 0

# now pick the best window optimizing the sum
for window in all_windows:
    profit = 0
    for win_map in agg:
        profit += win_map.get(window, 0)
    if profit > best_profit:
        best_profit = profit
        best_window = window

# 1955 too high
print(best_profit, best_window)
