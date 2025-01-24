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


def strength(cycle):
    return cycle * values[cycle - 1]


for idx in range(len(values)):
    print('#%d: %d' % (idx, values[idx]))

result = 0
for cycle in range(20, 220 + 1, 40):
    result += strength(cycle)
print(result)
