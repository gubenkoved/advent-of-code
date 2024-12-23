import itertools
import json
from collections import defaultdict

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
    data = {
        "nodes": [],
        "links": [],
    }

    for node in adjacency:
        data["nodes"].append({
            'id': node,
            'label': node,
            'color': '#0390fc' if node not in biggest else 'red',
        })
        for neighbor in adjacency[node]:
            if neighbor > node:
                continue
            data["links"].append({
                'source': node,
                'target': neighbor,
            })


    with open('graph.html', 'w') as f:
        graph_json = json.dumps(data)
        f.write(
"""
<html>
<head>
    <script src="https://unpkg.com/force-graph"></script>
</head>
<body>
    <div id="graph"></div>
    <script>
        const data = ##JSON##;
    </script>
    <script>
        const myGraph = new ForceGraph(document.getElementById('graph'))
            .graphData(data)
            // .nodeCanvasObjectMode(() => 'after')
            .nodeCanvasObject((node, ctx, globalScale) => {
              const label = node.id;
              const fontSize = 14 / globalScale;
              ctx.font = `${fontSize}px Sans-Serif`;
              const textWidth = ctx.measureText(label).width;
              const bckgDimensions = [textWidth, fontSize].map(n => n + fontSize * 0.2); // some padding
    
              ctx.fillStyle = 'rgba(255, 255, 255, 0.8)';
              ctx.fillRect(node.x - bckgDimensions[0] / 2, node.y - bckgDimensions[1] / 2, ...bckgDimensions);
    
              ctx.textAlign = 'center';
              ctx.textBaseline = 'middle';
              ctx.fillStyle = node.color;
              ctx.fillText(label, node.x, node.y);
    
              node.__bckgDimensions = bckgDimensions; // to re-use in nodePointerAreaPaint
            });
    </script>
</body>
</html>
""".replace('##JSON##', graph_json)
)


print(len(biggest))
print(','.join(sorted(biggest)))

visualize()
