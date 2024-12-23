from collections import defaultdict

file = open('data.txt', 'r')

adjacency = defaultdict(list)

for line in file:
    a, b = line.strip().split('-')
    adjacency[a].append(b)
    adjacency[b].append(a)


def traverse(node):
    walked = set()

    def walk(node):
        if node in walked:
            return
        walked.add(node)
        for neighbor in adjacency[node]:
            walk(neighbor)

    walk(node)

    return walked


connected_components = []
visited = set()

for node in adjacency:
    if node not in visited:
        component = traverse(node)
        visited.update(component)
        connected_components.append(component)


duplicates = set()
count = 0
for c in adjacency:
    for a in adjacency[c]:
        for b in adjacency[c]:
            if b not in adjacency[a]:
                continue
            if len(set([a, b, c])) < 3:
                continue
            key = tuple(sorted([a, b, c]))
            if key in duplicates:
                continue
            duplicates.add(key)
            print(key)
            if any(x.startswith('t') for x in [a, b, c]):
                count += 1

print(count)
