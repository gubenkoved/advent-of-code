values = []

with open('data.txt', 'r') as file:
    is_eof = False
    while not is_eof:
        current = []

        while True:
            line = file.readline()

            if not line:
                is_eof = True
                break
            elif line == '\n':
                break

            current.append(int(line.strip()))

        values.append(current)

sums = [sum(v) for v in values]
print(max(sums))

sums.sort()

print(sum(sums[-3:]))
