file = open('data.txt', 'r')

available = [x.strip() for x in file.readline().split(',')]

_ = file.readline()

needed = []

while True:
    line = file.readline()
    if not line:
        break
    needed.append(line.strip())


def is_possible(design):
    if not design:
        return True

    for prefix in available:
        if design.startswith(prefix):
            if is_possible(design[len(prefix):]):
                return True
    return False


print(sum(1 for design in needed if is_possible(design)))
