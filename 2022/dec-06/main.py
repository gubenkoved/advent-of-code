with open('data.txt', 'r') as file:
    line = file.readline().strip()


def solve(k):
    buffer = line[:k]

    for idx in range(k, len(line)):
        buffer += line[idx]
        buffer = buffer[1:]
        if len(set(buffer)) == k:
            print(idx + 1)
            break

solve(4)
solve(14)
