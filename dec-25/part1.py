import copy
from collections import defaultdict, deque
import itertools

adjacency = defaultdict(set)

with open('data.txt', 'r') as f:
    while True:
        line = f.readline()
        if not line:
            break
        line = line.strip()
        from_, to_ = line.split(':')

        for item in to_.strip().split(' '):
            adjacency[from_].add(item)
            adjacency[item].add(from_)


# import in Gephi!
with open('edges.csv', 'w') as f:
    f.write('source, target\n')
    for from_ in adjacency:
        for to_ in adjacency[from_]:
            f.write('%s, %s\n' % (from_, to_))

# algorithm
# repeat for 3 times
#   find most distant nodes in the graph
#   remove the shortest path from most distant nodes
#   this part is guaranteed to include our "bridge"
#   remove the edges on shortest path
# now all the removed edges are to be considered, but there are only a handful of them now
# in original graph try to remove any 3-combination and see if we get our graph split in two


def find_most_distant_from(adjacency, source):
    queue = deque()
    queue.append(source)
    visited = set()
    cur = None
    while queue:
        cur = queue.popleft()
        if cur in visited:
            continue
        visited.add(cur)
        for neighbor in adjacency[cur]:
            if neighbor not in visited:
                queue.append(neighbor)
    # we can just return latest node we visited actually...
    assert cur is not None
    return cur


def find_most_distant_nodes_pair(adjacency):
    nodes = list(adjacency.keys())
    # pick any node
    a = nodes[0]
    b = find_most_distant_from(adjacency, a)
    c = find_most_distant_from(adjacency, b)
    return b, c


def find_shortest_path_between(adjacency, start, end):
    queue = deque()
    queue.append(start)
    visited = set()
    prev = {}  # node -> prev node

    while queue:
        cur = queue.popleft()
        if cur in visited:
            continue
        visited.add(cur)
        for neighbor in adjacency[cur]:
            if neighbor not in visited:
                queue.append(neighbor)
                prev[neighbor] = cur

    # trace path back
    path = []
    cur = end
    while cur:
        path.append(cur)
        cur = prev.get(cur, None)
    return list(reversed(path))


def components(adjacency):
    nodes = list(adjacency.keys())
    result = []
    overall_visited = set()

    def traverse_from(node):
        queue = deque()
        queue.append(node)
        visited = set()
        while queue:
            cur = queue.popleft()
            if cur in visited:
                continue
            visited.add(cur)
            for neighbor in adjacency[cur]:
                if neighbor not in visited:
                    queue.append(neighbor)
        return visited

    for node in nodes:
        if node in overall_visited:
            continue
        visited = traverse_from(node)
        overall_visited.update(visited)
        result.append(visited)

    return result


mutable_adjacency = copy.deepcopy(adjacency)
removed_edges = []  # list of lists for removed edges in each round


def remove_edge(adjacency, from_, to_):
    adjacency[from_].discard(to_)
    adjacency[to_].discard(from_)


for _ in range(3):
    a, b = find_most_distant_nodes_pair(mutable_adjacency)
    path = find_shortest_path_between(mutable_adjacency, a, b)
    removed_in_round = []
    for idx in range(1, len(path)):
        from_, to_ = path[idx-1], path[idx]
        removed_in_round.append((from_, to_))
        remove_edge(mutable_adjacency, from_, to_)
    removed_edges.append(removed_in_round)


# optional optimization: for removed edges check starting from the center as
# obviously it is not the edges on the sides to be removed
def reorder(items):
    mid = len(items) // 2
    left = list(reversed(items[:mid]))
    right = items[mid:]
    result = []
    left_iter = iter(left)
    right_iter = iter(right)
    active = [left_iter, right_iter]
    while active:
        for iterator in list(active):
            try:
                element = next(iterator)
                result.append(element)
            except StopIteration:
                active.remove(iterator)
    return result


removed_edges = [reorder(x) for x in removed_edges]

# try to remove now
for e1, e2, e3 in itertools.product(*removed_edges):
    mutable_adjacency = copy.deepcopy(adjacency)

    print('checking (%s, %s, %s)' % (e1, e2, e3))

    remove_edge(mutable_adjacency, e1[0], e1[1])
    remove_edge(mutable_adjacency, e2[0], e2[1])
    remove_edge(mutable_adjacency, e3[0], e3[1])

    comp = components(mutable_adjacency)

    assert len(comp) <= 2

    if len(comp) == 2:
        print('can remove %s, %s and %s to get two components of size %s and %s' % (
            e1, e2, e3, len(comp[0]), len(comp[1])))
        break
