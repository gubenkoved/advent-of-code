from functools import lru_cache


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

    expanded_data = []
    for springs, group_sizes in data:
        expanded_data.append(
            ('?'.join(springs for _ in range(5)), group_sizes * 5),
        )

    def possible_arrangements(springs, group_sizes):
        print('solving for %s %s' % (springs, group_sizes))

        @lru_cache(maxsize=None)
        def count(springs, group_sizes):
            # end conditions
            if not springs and not group_sizes:
                return 1  # matched
            if not springs:
                return 0
            if not group_sizes:
                return all(c != '#' for c in springs)

            if springs[0] == '.':
                return count(springs[1:], group_sizes)

            assert springs[0] != '.'
            group_size = group_sizes[0]

            result = 0

            first_explicit_spring_idx = None
            for idx, c in enumerate(springs):
                if c == '#':
                    first_explicit_spring_idx = idx
                    break

            group_start_max = len(springs) - group_size

            if first_explicit_spring_idx is not None:
                group_start_max = min(group_start_max, first_explicit_spring_idx)

            # recursive dive
            for group_start_idx in range(group_start_max + 1):
                # try to start group here by checking that we can lay required number
                # of springs starting from here, and it will end with either '?' or '.'
                is_possible = True
                for cursor in range(group_start_idx, group_start_idx + group_size):
                    if springs[cursor] == '.':
                        is_possible = False
                        break

                # check chart after the group end
                if group_start_idx + group_size < len(springs) and springs[group_start_idx + group_size] not in ('?', '.'):
                    is_possible = False

                if is_possible:
                    # +1 because next char after the group has to be "."
                    result += count(springs[group_start_idx + group_size + 1:], tuple(group_sizes[1:]))

            return result

        return count(springs, tuple(group_sizes))

    result = 0

    for springs, group_sizes in expanded_data:
        result += possible_arrangements(springs, group_sizes)

    print(result)
