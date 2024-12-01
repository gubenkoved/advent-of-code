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
        cur = 'AAA'
        n = len(steps)

        while True:
            direction = steps[steps_count % n]

            if direction == 'L':
                cur = m[cur][0]
            else:
                cur = m[cur][1]

            steps_count += 1

            if cur == 'ZZZ':
                break

        print('took %d steps' % steps_count)
