file = open('data.txt', 'r')

stones = [int(x) for x in file.readline().split( )]


def step(stones):
    result = []

    for stone in stones:
        if stone == 0:
            result.append(1)
        elif len(str(stone)) % 2 == 0:
            s = str(stone)
            left = s[:len(s) // 2]
            right = s[len(s) // 2:]
            result.append(int(left))
            result.append(int(right))
        else:
            result.append(stone * 2024)
    return result


for idx in range(1, 25 + 1):
    stones = step(stones)
    # print(stones)
    print('after step #%s: %s' % (idx, len(stones)))

print(len(stones))
