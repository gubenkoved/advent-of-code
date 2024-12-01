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

        cycles = []

        # compute cycles
        for cur in cur_set:
            # print('Compute cycle that starts with %s...' % cur)
            cursor = cur
            step_counter = 0
            cycle = [
                (cur, 0)
            ]

            while True:
                direction = steps[step_counter % n]
                cursor = m[cursor][0] if direction == 'L' else m[cursor][1]
                step_counter += 1

                next_state = (cursor, step_counter % n)

                if next_state in cycle:
                    offset = cycle.index(next_state)
                    z_index = None
                    for node_idx, (node, _) in enumerate(cycle):
                        if node.endswith('Z'):
                            assert z_index is None
                            z_index = node_idx
                    z_offset = z_index - offset
                    print('Cycle found! Full Len %d, Cycle Offset %d, Cycle Len %d, Z offset %d, Z index %d' % (
                        len(cycle), offset, len(cycle) - offset, z_offset, z_index))
                    cycles.append(cycle)
                    break

                cycle.append((cursor, step_counter % n))

        # it turns out that z_index == cycle len! why though?
        # it simplifies the computation
        # then go to wolframalpha
        # lcm(18157, 11653, 21409, 12737, 14363, 15989)
        # result: 9064949303801
        # .. or actually use math.lcm()

        # for cycle_idx, cycle in enumerate(cycles):
        #     cycle_nodes = [t[0] for t in cycle]
        #     print('Unique nodes in cycle %d: %d' % (cycle_idx, len(set(cycle_nodes))))

        # print('compute nodes usage in cycles...')
        # for node in m:
        #     cycle_idxs = []
        #     for cycle_idx, cycle in enumerate(cycles):
        #         if node in cycle:
        #             cycle_idxs.append(cycle_idx)
        #     print('%s used in cycles: %s' % (node, cycle_idxs))

        # print('print cycles...')
        # for cycle_idx, cycle in enumerate(cycles):
        #     print('cycle #%d, len %d' % (cycle_idx, len(cycle)))
        #     cycle_nodes = [t[0] for t in cycle]
        #     print(' '.join(cycle_nodes))

