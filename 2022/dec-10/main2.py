operations = []

with open('data.txt', 'r') as file:
    while True:
        line = file.readline()

        if not line:
            break

        operations.append(line.strip().split(' '))

values = []
value = 1
values.append(value)

for operation in operations:
    op = operation[0]

    if op == 'noop':
        values.append(value)
    elif op == 'addx':
        arg = int(operation[1])
        values.append(value)
        values.append(value + arg)
        value += arg


for idx in range(len(values)):
    print('#%d: %d' % (idx, values[idx]))

for cycle in range(1, 240 + 1):
    x = values[cycle]
    crt_x = 1 + (cycle - 1) % 40
    is_lit = abs(crt_x - x) <= 1
    print('#' if is_lit else '.', end='')
    if cycle % 40 == 0:
        print()

# answer is EGJBGCFK
# for some reason first column appears to be broken...
