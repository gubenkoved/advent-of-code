import re
import json

valves = {}

with open('data.txt', 'r') as file:
    while True:

        line = file.readline()

        if not line:
            break

        match = re.match('Valve ([A-Z]+) has flow rate=([0-9]+); tunnels? leads? to valves? (.+)', line.strip())

        assert match

        valves[match.group(1)] = (
            int(match.group(2)),
            tuple(x.strip() for x in match.group(3).split(',')),
        )


nodes = []
links = []


for valve, (flow_rate, neighbors) in valves.items():
    nodes.append({
        'id': valve,
        'flow_rate': flow_rate,
        'color': 'red' if flow_rate else 'green',
        'text': f'{valve} ({flow_rate})',
    })
    for neighbor in neighbors:
        links.append({
            'source': valve,
            'target': neighbor,
        })


html = ("""
<html>
<head>
    <script src="https://unpkg.com/force-graph"></script>
</head>
<body>
<div id="target"></div>
<script>
    const nodes = JSON.parse(##nodes##);
    const links = JSON.parse(##links##);

    const targetDiv = document.getElementById("target");
    const myGraph = new ForceGraph(targetDiv)
        .graphData({
            nodes,
            links,
        })
        .nodeCanvasObject((node, ctx, globalScale) => {
          const label = node.text;
          const fontSize = 12/globalScale;
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
        })
        .nodePointerAreaPaint((node, color, ctx) => {
          ctx.fillStyle = color;
          const bckgDimensions = node.__bckgDimensions;
          bckgDimensions && ctx.fillRect(node.x - bckgDimensions[0] / 2, node.y - bckgDimensions[1] / 2, ...bckgDimensions);
        });
</script>
</body>
</html>
"""
        .replace('##nodes##', json.dumps(json.dumps(nodes)))
        .replace('##links##', json.dumps(json.dumps(links)))
)


with open('vis.html', 'w') as file:
    file.write(html)
