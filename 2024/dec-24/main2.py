import collections
import functools
import re
import json
import random

file = open('data.txt', 'r')

gates = []

# skip the values section now
while True:
    line = file.readline()
    if line == '\n':
        break

# read gates
while True:
    line = file.readline()

    if not line:
        break

    match = re.match('([a-z0-9]+) (OR|XOR|AND) ([a-z0-9]+) -> ([a-z0-9]+)', line)

    assert match is not None

    gates.append([
        match.group(1),
        match.group(2),
        match.group(3),
        match.group(4),
    ])


class Simulator:
    def __init__(self, gates):
        # name -> operation
        self.gate_types = {}
        # name -> input names
        self.in_map = collections.defaultdict(list)
        # name -> output names
        self.out_map = collections.defaultdict(list)

        # process gates
        for a, op, b, r in gates:
            assert r not in self.gate_types
            self.gate_types[r] = op

            self.in_map[r].append(a)
            self.in_map[r].append(b)

            self.out_map[a].append(r)
            self.out_map[b].append(r)

        # sanity checks
        for gate in self.in_map:
            # only two inputs are for each gate
            assert len(self.in_map[gate]) == 2

    def swap(self, gate1, gate2):
        # update gate type
        self.gate_types[gate1], self.gate_types[gate2] = self.gate_types[gate2], self.gate_types[gate1]
        # update adjacency
        self.in_map[gate1], self.in_map[gate2] = self.in_map[gate2], self.in_map[gate1]
        self.out_map[gate1], self.out_map[gate2] = self.out_map[gate2], self.out_map[gate1]

    def has_cycles(self):
        visited = set()
        stack = set()

        # returns true if cycle is detected
        def dfs(name: str) -> bool:
            if name in stack:
                return True
            if name in visited:
                return False
            visited.add(name)
            stack.add(name)
            for in_gate in self.in_map.get(name, []):
                if dfs(in_gate):
                    return True
            stack.discard(name)
            return False

        for name in self.gate_types:
            if dfs(name):
                return True

        return False

    def distances_from(self, name, use_out=False):
        queue = [(name, 0)]
        dist_map = {}
        visited = set()
        while queue:
            cur, dist = queue.pop(0)
            if cur in visited:
                continue
            visited.add(cur)
            dist_map[cur] = dist
            adjacent = self.in_map.get(cur, [])
            if use_out:
                adjacent += self.out_map.get(cur, [])
            for name in adjacent:
                queue.append((name, dist + 1))
        return dist_map

    def sim(self, value_map):
        @functools.cache
        def value_of(name):
            if name in value_map:
                return value_map[name]

            assert name in self.gate_types
            op = self.gate_types[name]

            if op == 'AND':
                result = True
                for in_gate in self.in_map[name]:
                    result &= value_of(in_gate)
            elif op == 'OR':
                result = False
                for in_gate in self.in_map[name]:
                    result |= value_of(in_gate)
            elif op == 'XOR':
                result = False
                for in_gate in self.in_map[name]:
                    result ^= value_of(in_gate)

            return result

        result_map = {}
        for gate, op in self.gate_types.items():
            result_map[gate] = value_of(gate)
        return result_map

    def set_inout_register(self, reg_map, number, prefix):
        for idx in range(45):
            reg_map['%s%02d' % (prefix, idx)] = number % 2
            number //= 2

    def get_output(self, values_map):
        result = 0
        for idx in range(46):
            if values_map['z%02d' % idx]:
                result |= 1 << idx
        return result

    def sim2(self, x, y):
        reg_map = {}
        self.set_inout_register(reg_map, x, 'x')
        self.set_inout_register(reg_map, y, 'y')
        result_map = self.sim(reg_map)
        return self.get_output(result_map)

    def is_correct2(self):
        # try setting par of bits at all possible places
        for x_idx in range(45):
            for y_idx in range(45):
                x = 1 << x_idx
                y = 1 << y_idx
                result = self.sim2(x, y)
                if result != x + y:
                    print(' WA when x=%d, y=%d, got %d, expected %d' % (x, y, result, x + y))
                    return False
        return True

    # probability based
    def is_correct(self):
        for _ in range(10):
            x = random.randint(0, 2 ** 44 - 1)
            y = random.randint(0, 2 ** 44 - 1)
            result = self.sim2(x, y)
            if result != x + y:
                print(' WA when x=%d, y=%d, got %d, expected %d' % (x, y, result, x + y))
                return False
        return True


def visualize():
    nodes = {}
    links = []

    color_map = {
        'AND': 'red',
        'OR': 'green',
        'XOR': 'blue',
    }

    for a, op, b, r in gates:
        if a not in nodes:
            nodes[a] = {
                'id': a,
                'label': a,
                'color': 'black',
            }
        if b not in nodes:
            nodes[b] = {
                'id': b,
                'label': b,
                'color': 'black',
            }
        nodes[r] = {
            'id': r,
            'label': '%s %s' % (r, op),
            'color': color_map[op],
        }

        links.append({
            'source': a,
            'target': r,
        })
        links.append({
            'source': b,
            'target': r,
        })
    visualize_impl(nodes, links, 'graph.html')


def visualize2():
    nodes = {}
    links = []

    color_map = {
        'AND': 'red',
        'OR': 'green',
        'XOR': 'blue',
    }
    for a, op, b, r in gates:
        if a not in nodes:
            nodes[a] = {
                'id': a,
                'label': a,
                'color': 'black',
            }
        if b not in nodes:
            nodes[b] = {
                'id': b,
                'label': b,
                'color': 'black',
            }
        nodes[r] = {
            'id': r,
            'label': r,
            'color': 'black',
        }
        op_id = '%s-%s-%s' % (a, op, b)
        nodes[op_id] = {
            'id': op_id,
            'label': op,
            'color': color_map[op],
        }
        links.append({
            'source': a,
            'target': op_id,
        })
        links.append({
            'source': b,
            'target': op_id,
        })
        # labeling link
        links.append({
            'source': op_id,
            'target': r,
            'dashed': True,
        })
    visualize_impl(nodes, links, 'graph2.html')


def visualize_impl(nodes, links, path):
    data = {
        'nodes': list(nodes.values()),
        'links': links,
    }
    with open(path, 'w') as f:
        graph_json = json.dumps(data)
        f.write(
            """
            <html>
            <head>
                <script src="https://unpkg.com/force-graph"></script>
                <script src="https://cdnjs.cloudflare.com/ajax/libs/d3/7.9.0/d3.js"></script>
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
                        .linkDirectionalArrowLength(8)
                        .nodeVal(1)
                        .linkLineDash(link => link.dashed && [4, 4])
                        .nodeCanvasObject((node, ctx, globalScale) => {
                          const label = node.label;
                          const fontSize = 14 / globalScale;
                          ctx.font = `${fontSize}px Sans-Serif`;
                          const textWidth = ctx.measureText(label).width;
                          const bckgDimensions = [textWidth, fontSize].map(n => n + fontSize * 0.4);
        
                          ctx.fillStyle = 'rgba(255, 255, 255, 0.5)';
                          ctx.fillRect(node.x - bckgDimensions[0] / 2, node.y - bckgDimensions[1] / 2, ...bckgDimensions);
                          ctx.strokeStyle = 'rgba(0, 0, 0, 0.2)';
                          ctx.lineWidth = 1 / globalScale;
                          ctx.strokeRect(node.x - bckgDimensions[0] / 2, node.y - bckgDimensions[1] / 2, ...bckgDimensions);
        
                          ctx.textAlign = 'center';
                          ctx.textBaseline = 'middle';
                          ctx.fillStyle = node.color;
                          ctx.fillText(label, node.x, node.y);
        
                          node.__bckgDimensions = bckgDimensions; // to re-use in nodePointerAreaPaint
                        });

                    function changeForces() {
                        myGraph.d3Force("link", d3.forceLink(data.links).id(d => d.id));
                        myGraph.d3Force("charge", d3.forceManyBody().strength(-100));
                        myGraph.d3Force("x", d3.forceX());
                        myGraph.d3Force("y", d3.forceY());
                        myGraph.d3ReheatSimulation();
                    }
                    // setTimeout(changeForces, 3000);
                </script>
            </body>
            </html>
            """.replace('##JSON##', graph_json)
        )

# just look at the graph!
# (z18, hmt)
# (bfq, z27)
# (z31, hkh)
# (bng, fjp)
# bfq,bng,fjp,hkh,hmt,z18,z27,z31
visualize()
visualize2()

simulator = Simulator(gates)

print('initially circuit is not good, see: ')
assert simulator.is_correct() == False
assert simulator.has_cycles() == False

dist_map = simulator.distances_from('z45', use_out=True)

# sort gates by distance from the last one (desc)
gates = sorted(gates, key=lambda x: dist_map.get(x[-1], float('inf')), reverse=True)
for a, op, b, r in gates:
    suffix = ' *** ' if r.startswith('z') else ''
    print('%3.0f  |  %3s %3s %3s -> %3s%s' % (dist_map.get(r, float('inf')), a, op, b, r, suffix))

print('\n***\n')
for idx in range(45 + 1):
    gate = 'z%02d' % idx
    # show up to 3 levels of the inputs
    dist_map = simulator.distances_from(gate, use_out=True)
    for d in range(3 + 1):
        for a, op, b, r in sorted(gates, key=lambda g: g[1]):
            if dist_map.get(r) != d:
                continue
            print('%3d  |  %3s %3s %3s -> %3s' % (dist_map[r], a, op, b, r))
    print('')

n = len(gates)

# try fixing with very limited the max "distance" between error gates
def fix(swaps, max_swaps, max_dist):
    if len(swaps) == max_swaps:
        print('checking for swaps: %s' % swaps)
        if simulator.has_cycles():
            print('  cycles detected')
        else:
            if simulator.is_correct():
                print('fixed! swaps: %s' % swaps)
                exit(0)
    else:  # recursion step
        start_idx = 0 if not swaps else swaps[-1][1] + 1
        for idx1 in range(start_idx, n):
            for idx2 in range(idx1 + 1, n):
                if idx2 - idx1 > max_dist:
                    continue
                g1, g2 = gates[idx1], gates[idx2]
                simulator.swap(g1[-1], g2[-1])
                fix(swaps + [(idx1, idx2)], max_swaps, max_dist)
                simulator.swap(g1[-1], g2[-1])


# FIXME: still too long...
# print('fixing...')
# fix([], max_swaps=4, max_dist=10)

# TODO: use pattern to check all summators except first two and the last one
# XOR Z_n
#     OR # carryover
#         AND
#             X_n-1
#             Y_n-1
#         AND
#             OR  # prev carryover
#             XOR
#     XOR
#         X_n
#         Y_n
