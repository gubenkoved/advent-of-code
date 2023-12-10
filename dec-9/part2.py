
if __name__ == '__main__':
    numbers = []

    with open('data.txt', 'r') as f:
        while True:
            line = f.readline()

            if not line:
                break

            numbers.append([int(x) for x in line.split(' ')])

    # returns next number
    def extrapolate(a):
        print('extrapolating %s' % a)

        levels = [a]

        # forward pass
        while True:
            cur_level = levels[-1]
            next_level = []

            zeros = True
            for idx in range(1, len(cur_level)):
                d = cur_level[idx] - cur_level[idx - 1]

                if d != 0:
                    zeros = False

                next_level.append(d)

            levels.append(next_level)

            if zeros:
                break

        # backward pass
        levels[-1].append(0)

        for level_num in range(len(levels) - 2, -1, -1):
            diff = levels[level_num + 1][-1]
            levels[level_num].append(levels[level_num][-1] + diff)

        return levels[0][-1]

    result = 0
    for seq in numbers:
        result += extrapolate(list(reversed(seq)))

    print(result)
