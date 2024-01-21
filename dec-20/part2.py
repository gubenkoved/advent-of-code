import os.path
from collections import namedtuple, defaultdict, deque
from typing import Dict
import pyvis.network

ModuleDef = namedtuple('ModuleDef', ['type', 'outputs'])


LOW = 'low'
HIGH = 'high'


class FlipFlopState:
    def __init__(self, state):
        self.state = state


class ConjunctionState:
    def __init__(self, input_states):
        self.input_states = input_states


if __name__ == '__main__':
    modules: Dict[str, ModuleDef] = {}
    with open('data.txt', 'r') as f:
        while True:
            line = f.readline()
            if not line:
                break

            name, outputs = line.split(' -> ')
            outputs_names = [x.strip() for x in outputs.split(',')]

            if name[0] in ['%', '&']:
                modules[name[1:]] = ModuleDef(name[0], outputs_names)
            else:
                modules[name] = ModuleDef('broadcaster', outputs_names)

    # add dummy modules referenced in output, but not present in wiring
    for module in list(modules.values()):
        for output_name in module.outputs:
            if output_name not in modules:
                modules[output_name] = ModuleDef('dummy', [])

    # inputs map module name -> list of input module names
    inputs = defaultdict(list)
    for module_name, module_def in modules.items():
        for output_module_name in module_def.outputs:
            inputs[output_module_name].append(module_name)

    def visualize():
        # visualize with pyvis
        g = pyvis.network.Network(
            # 100% does not render properly for height...
            height='1000px', width='100%',
            directed=True,
        )
        for module in modules:
            color = '#4f4f4f'  # gray-ish
            if modules[module].type == '%':
                color = '#a12a69'  # red-ish
            elif modules[module].type == '&':
                color = '#3273a8'  # blue-ish
            g.add_node(
                n_id=module,
                label=module,
                color=color,
                font='20px Ubuntu black',
            )

        # create edges
        for module in modules:
            for out_module in modules[module].outputs:
                g.add_edge(
                    source=module,
                    to=out_module,
                    # arrowStrikethrough=True,
                )
        g.show('graph.html', notebook=False)

    if not os.path.exists('graph.html'):
        visualize()

    # initialize state map
    state_map = {}

    for module_name, module_def in modules.items():
        if module_def.type == '%':
            state_map[module_name] = FlipFlopState(LOW)
        elif module_def.type == '&':
            state_map[module_name] = ConjunctionState({
                input_name: LOW for input_name in inputs[module_name]
            })

    # simulate low pulse propagation using BFS type of traversal

    # (source, pulse type, target)
    # pulses = []

    def flip(state):
        return HIGH if state == LOW else LOW

    rx_signaled = False
    pulses = []

    def simulate_one():
        global rx_signaled

        # (source, pulse type, target)
        active_queue = deque()

        active_queue.append(
            ('button', LOW, 'broadcaster'),
        )

        while active_queue:
            source, pulse, target = active_queue.popleft()
            pulses.append((source, pulse, target))

            if target == 'rx' and pulse == LOW:
                rx_signaled = True

            if modules[target].type == '%':  # flip-flop
                if pulse == LOW:
                    # flip-flop flips!
                    state_map[target].state = flip(state_map[target].state)
                    for output_module in modules[target].outputs:
                        active_queue.append(
                            (target, state_map[target].state, output_module)
                        )
                else:
                    # on high pulse flip-flop does nothing
                    pass
            elif modules[target].type == '&':  # conjunction
                # update state
                state_map[target].input_states[source] = pulse

                if all(p == HIGH for p in state_map[target].input_states.values()):
                    conjunction_out = LOW
                else:
                    conjunction_out = HIGH

                # send out pulse
                for output_module in modules[target].outputs:
                    active_queue.append(
                        (target, conjunction_out, output_module)
                    )
            elif modules[target].type == 'broadcaster':
                for output_module in modules[target].outputs:
                    active_queue.append(
                        (target, LOW, output_module)
                    )
            elif modules[target].type == 'dummy':
                pass

    press_count = 0
    while not rx_signaled:
        press_count += 1
        simulate_one()

        # see graph visualization
        for key_module in ['qs', 'pg', 'sv', 'sp']:
            if any(pulse == HIGH and source == key_module for source, pulse, target in pulses):
                print('[%s] HIGH pulse after %s presses' % (key_module, press_count))

        pulses.clear()

        if press_count == 10000:
            break

    # periods from output above:
    # qs: 4051
    # pg: 3761
    # sv: 3919
    # sp: 3907
    import math
    print(math.lcm(4051, 3761, 3919, 3907))
