if __name__ == '__main__':

    data = []
    with open('data.txt', 'r') as f:
        while True:
            line = f.readline()
            if not line:
                break
            springs, groups_text = line.strip('\n').split(' ')
            group_sizes = [int(x) for x in groups_text.split(',')]
            data.append(
                (springs, group_sizes)
            )

    print('max spring size')
    print(max(len(x[0]) for x in data))
    print('max unknowns size')  # 19
    print(max(sum(1 for c in x[0] if c == '?') for x in data))

    # 19 unknowns give us only 2^19 combinations to check

    def possible_arrangements(springs, group_sizes):
        possible = 0

        def search(cur):
            nonlocal possible

            if len(cur) == len(springs):
                actual_sizes = [len(g) for g in cur.split('.') if g != '']

                if actual_sizes == group_sizes:
                    possible += 1

                return

            idx = len(cur)
            if springs[idx] != '?':
                search(cur + springs[idx])
            else:
                search(cur + '.')
                search(cur + '#')

        search('')

        return possible

    result = 0

    for springs, group_sizes in data:
        result += possible_arrangements(springs, group_sizes)

    print(result)
