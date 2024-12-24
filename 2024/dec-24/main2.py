import re
import json


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

    gates.append((
        match.group(1),
        match.group(2),
        match.group(3),
        match.group(4)
    ))


class CycleFound(Exception):
    pass


class Simulator:
    def __init__(self, gates):
        self.gates = gates
        self.gates_map = {}
        self.value_map = {}
        for a, op, b, r in gates:
            assert r not in self.gates_map
            self.gates_map[r] = (a, op, b)
        # gate -> value
        self.cache = {}

    # TODO: build dependency map using disjoint set?
    def swap(self, idx1, idx2):
        gate1 = gates[idx1]
        gate2 = gates[idx2]

        tmp = self.gates_map[gate1[-1]]
        self.gates_map[gate1[-1]] = self.gates_map[gate2[-1]]
        self.gates_map[gate2[-1]] = tmp

        # TODO: invalidate only affected ones (outputs) recursively
        #  and the outputs where invalid are input
        # clear the cache
        self.cache.clear()

    # TODO: cache values on individual gates based on state of the inputs,
    #   no changes in inputs -> no changes in the outputs
    def calculate(self, reg):
        return self.calculate_impl(reg, set())

    def calculate_impl(self, reg, dependent: set):
        if reg in dependent:
            raise CycleFound()

        if reg in self.value_map:
            return self.value_map[reg]

        # do not recalculate the same intermediary register multiple times
        if reg in self.cache:
            return self.cache[reg]

        a, op, b = self.gates_map[reg]

        dependent = dependent | { reg }

        if op == 'OR':
            result = self.calculate_impl(a, dependent) | self.calculate_impl(b, dependent)
        elif op == 'XOR':
            result = self.calculate_impl(a, dependent) ^ self.calculate_impl(b, dependent)
        elif op == 'AND':
            result = self.calculate_impl(a, dependent) & self.calculate_impl(b, dependent)
        else:
            assert False

        self.cache[reg] = result
        return result

    # passes x and y to circuits and computes z
    def sim(self, x, y):
        for idx in range(45):
            self.value_map['x%02d' % idx] = x % 2
            x = x // 2
        for idx in range(45):
            self.value_map['y%02d' % idx] = y % 2
            y = y // 2
        # capture the result
        z = 0
        for idx in range(46):
            zv = self.calculate('z%02d' % idx)
            z |= zv << idx
        return z

    def check_circuit2(self):
        error_count = 0
        for x_bit in range(45):
            for y_bit in range(45):
                x = 1 << x_bit
                y = 1 << y_bit
                z = self.sim(x, y)
                good = z == x + y
                if not good:
                    # print('%d + %d -> %d (%s)' % (x, y, z, 'OK' if good else 'ERR'))
                    error_count += 1
        return error_count

    def check_circuit(self):
        try:
            return self.check_circuit2()
        except CycleFound:
            print('cycle found')
            return float('+inf')


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
    data = {
        'nodes': list(nodes.values()),
        'links': links,
    }

    with open('graph.html', 'w') as f:
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
                        .nodeCanvasObject((node, ctx, globalScale) => {
                          const label = node.label;
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
# bfq,bng,fjp,hkh,hmt,z18,z27,z31
visualize()

# simulator = Simulator(gates)
#
# # initially broken
# assert simulator.check_circuit() > 0
#
# n = len(gates)
#
#
# # backtracking search to find all the 4 broken ones
# def finder(swaps, swapped_indexes):
#     print('checking with swaps %r' % swaps)
#
#     # by definition, there are  4 pairs of gates that are swapped
#     if len(swaps) == 4:
#         if simulator.check_circuit():
#             print('SOLVED! %r' % swaps)
#             return True
#     else:
#         # pick a pair to swap that reduces error count
#         baseline_error_count = simulator.check_circuit()
#         print('baseline error count: %r' % baseline_error_count)
#
#         for idx1 in range(n):
#             for idx2 in range(idx1 + 1, n):
#                 if idx1 in swapped_indexes:
#                     continue
#                 if idx2 in swapped_indexes:
#                     continue
#
#                 print('  trying swap (%d, %d)' % (idx1, idx2))
#                 simulator.swap(idx1, idx2)
#                 error_count = simulator.check_circuit()
#                 print('    new error count: %r' % error_count)
#
#                 # FIXME: this is a wrong assumption that we have a monotonically
#                 #  decreasing error count
#                 if error_count >= baseline_error_count:
#                     # swap back
#                     simulator.swap(idx1, idx2)
#                     continue
#
#                 swaps.append((idx1, idx2))
#                 swapped_indexes.add(idx1)
#                 swapped_indexes.add(idx2)
#                 finder(swaps, swapped_indexes)
#                 swaps.pop(-1)
#                 swapped_indexes.discard(idx1)
#                 swapped_indexes.discard(idx2)
#
#                 simulator.swap(idx1, idx2)
#
# finder([], set())
