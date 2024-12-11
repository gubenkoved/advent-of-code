import functools


file = open('data.txt', 'r')

stones = [int(x) for x in file.readline().split( )]


@functools.lru_cache(None)
def f(stone, rounds):
    if rounds == 0:
        return 1

    if stone == 0:
        return f(1, rounds - 1)
    elif len(str(stone)) % 2 == 0:
        s = str(stone)
        left = s[:len(s) // 2]
        right = s[len(s) // 2:]
        return f(int(left), rounds - 1) + f(int(right), rounds - 1)
    else:
        return f(stone * 2024, rounds - 1)

print(sum(f(stone, 75) for stone in stones))
