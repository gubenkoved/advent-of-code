file = open('data.txt', 'r')

seeds = [int(x) for x in file]


def mix(a, b):
    return a ^ b

def prune(a):
    return a % 16777216

def step(x):
    x = prune(mix(x, x * 64))
    x = prune(mix(x, x // 32))
    x = prune(mix(x, x * 2048))
    return x


result = 0
for seed in seeds:
    x = seed
    for _ in range(2000):
        x = step(x)
    result += x
    print(x)
print(result)