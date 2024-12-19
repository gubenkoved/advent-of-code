import functools

file = open('data.txt', 'r')

available = [x.strip() for x in file.readline().split(',')]

_ = file.readline()

needed = []

while True:
    line = file.readline()
    if not line:
        break
    needed.append(line.strip())


@functools.lru_cache(maxsize=None)
def count_ways(design):
    if not design:
        return 1

    result = 0
    for prefix in available:
        if design.startswith(prefix):
            result += count_ways(design[len(prefix):])
    return result


print(sum(count_ways(design) for design in needed))
