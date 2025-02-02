import functools
import re
import sys

valves = {}

source = sys.argv[1]

print('using source "%s"' % source)

with open(source, 'r') as file:
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


# define a function that will solve out problem, the parameters should define
# whole state of the system -- a point in phase space, so that we can solve big
# problem via solving subproblems
@functools.cache
def maximize(time_left, cur, opened):
    if time_left == 0:
        return 0

    # our strategy can be either:
    # 1. do nothing
    # 2. try to move to other valve to open other valves
    # 3. open current valve if it is not yet opened

    cur_flow_rate = sum(valves[valve][0] for valve in opened)

    options = [
        # stay w/o moving on the current valve
        maximize(time_left - 1, cur, opened)
    ]

    if cur not in opened and valves[cur][0] > 0:
        # we can try opening it
        options.append(
            maximize(time_left - 1, cur, opened + (cur,))
        )

    # or move elsewhere
    for neighbor in valves[cur][1]:
        options.append(
            maximize(time_left - 1, neighbor, opened)
        )

    return cur_flow_rate + max(options)


# data_1.txt -> 1229
# data_2.txt -> 1561

print(maximize(26, 'AA', tuple()))
