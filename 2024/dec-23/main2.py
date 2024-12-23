from collections import defaultdict
import pyvis
import itertools


file = open('data.txt', 'r')

adjacency = defaultdict(set)

for line in file:
    a, b = line.strip().split('-')
    adjacency[a].add(b)
    adjacency[b].add(a)


max_degree = 0
for node in adjacency:
    max_degree = max(max_degree, len(adjacency[node]))

print('max degree is ', max_degree)

def cluster_with(seed):
    neighbors = adjacency[seed]

    for cluster_size in range(len(neighbors), 0, -1):
        print('checking size ', cluster_size)
        for cluster2 in itertools.combinations(neighbors, cluster_size):
            cluster = set(cluster2) | {seed}

            # check that all nodes are adjacent to all in inside cluster
            ok = True
            for node in cluster:
                if not all(x in adjacency[node] for x in cluster if x != node):
                    ok = False
                    break
            if ok:
                return cluster

    assert False

biggest = set()
for node in adjacency:
    x = cluster_with(node)
    if len(x) > len(biggest):
        biggest = x


def visualize():
    g = pyvis.network.Network(
        # 100% does not render properly for height...
        height='1000px', width='100%',
        directed=True,
    )
    for node in adjacency:
        g.add_node(
            n_id=node,
            label=node,
            color='#0390fc' if node not in biggest else 'red',
            font='20px Ubuntu black',
        )

    # create edges
    for node in adjacency:
        for neighbor in adjacency[node]:
            if node > neighbor:
                continue
            g.add_edge(
                source=node,
                to=neighbor,
            )
    g.show('graph.html', notebook=False)

print(len(biggest))
print(','.join(sorted(biggest)))

visualize()
