if __name__ == '__main__':
    with open('data.txt', 'r') as f:
        steps = f.readline().rstrip()
        f.readline()

        # node -> (left, right)
        m = {}
        while True:
            line = f.readline().strip()

            if not line:
                break

            from_node, lr_nodes = line.split('=')
            lr_nodes2 = lr_nodes.strip(' ()').split(',')
            m[from_node.strip()] = (
                lr_nodes2[0].strip(),
                lr_nodes2[1].strip(),
            )

        # simulation phase
        steps_count = 0
        n = len(steps)
        cur_set = []

        for node in m:
            if node[-1] == 'A':
                cur_set.append(node)

        best_z_score = 0

        # compute cycles
        for cur in cur_set:
            print('Compute cycle that starts with %s' % cur)

            cursor = cur
            step_counter = 0
            states = set()
            states.add((cursor, step_counter))
            cycle = []
            cycle.append(cur)

            while True:
                direction = steps[step_counter % n]
                cursor = m[cursor][0] if direction == 'L' else m[cursor][1]
                step_counter += 1

                if (cursor, step_counter % n) in states:
                    print('Cycle found! Len %d' % len(cycle))
                    # print(cycle)
                    break
                else:
                    cycle.append(cursor)
                    states.add((cursor, step_counter % n))

        print('Run simulation...')

        while True:
            direction = steps[steps_count % n]

            next_cur_set = []
            for cur in cur_set:
                if direction == 'L':
                    next_cur_set.append(m[cur][0])
                else:
                    next_cur_set.append(m[cur][1])
            cur_set = next_cur_set

            steps_count += 1

            z_count = sum(1 for cur in cur_set if cur[-1] == 'Z')

            # print('STEP %6d: %s (Z-SCORE %d)' % (steps_count, cur_set, z_count))

            best_z_score = max(best_z_score, z_count)

            if steps_count % 100000 == 0:
                print('STEP %d, BEST Z SCORE %d' % (steps_count, best_z_score))

            if z_count == len(cur_set):
                break

        print('took %d steps' % steps_count)
