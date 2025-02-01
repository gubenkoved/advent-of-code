import functools
import re
import heapq

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



# returns shortest distance in hops from one valve to another
def distance(from_, to_):
    dist_map = distance_from(from_)
    return dist_map[to_]


@functools.cache
def distance_from(from_):
    visited = set()
    heap = [
        (0, from_)
    ]
    dist_map = {}

    while heap:
        dist, cur = heapq.heappop(heap)

        if cur in visited:
            continue

        visited.add(cur)
        dist_map[cur] = dist

        for neighbor in valves[cur][1]:
            heapq.heappush(heap, (dist + 1, neighbor))

    return dist_map



# define a function that will solve out problem, the parameters should define
# whole state of the system -- a point in phase space, so that we can solve big
# problem via solving subproblems

# actor1 and actor2 will now represent position and valve it is trying to get
# to shrink the search space, because it does not do any good to stay on the
# current place if there are not yet opened valves

# actor is a tuple of (target, time to target)

def st(iterable):
    return tuple(sorted(iterable))


EXHAUSTED = ('NONE', -2)


@functools.cache
def maximize(
        time_left: int,
        actor1: tuple[str, int],
        actor2: tuple[str, int],
        flow_rate: int,
        targets: tuple,
):
    if time_left == 0:
        return 0

    # our strategy is:
    # 1. do nothing if there are no more targets left
    # 2. open a valve for actor if we arrived to our target
    #    then target becomes None on that tick
    # 3. pick new target among available ones if no current target

    options = []

    # it takes 1 tick to open the valve, so we wait until -1 ticks are left
    # to the target to update the opened valves state
    actor1_valve, actor1_ttt = actor1
    actor2_valve, actor2_ttt = actor2

    if actor1_ttt == -1:
        # pick next targets
        for t in targets:
            options.append(
                maximize(
                    # notice we do not tick yet here!
                    time_left,
                    (t, distance(actor1_valve, t)),
                    actor2,
                    flow_rate + valves[actor1_valve][0],
                    st(set(targets) - {t}),
                )
            )
        else:
            options.append(
                maximize(
                    time_left,
                    EXHAUSTED,
                    actor2,
                    flow_rate + valves[actor1_valve][0],
                    tuple(),
                )
            )
    elif actor2_ttt == -1:
        # pick next targets
        for t in targets:
            options.append(
                maximize(
                    time_left,
                    actor1,
                    (t, distance(actor2_valve, t)),
                    flow_rate + valves[actor2_valve][0],
                    st(set(targets) - {t}),
                )
            )
        else:
            options.append(
                maximize(
                    time_left,
                    actor1,
                    EXHAUSTED,
                    flow_rate + valves[actor2_valve][0],
                    tuple(),
                )
            )

    # tick passing
    if not options:
        options.append(
            flow_rate + maximize(
                time_left - 1,
                (actor1_valve, actor1_ttt - 1) if actor1 != EXHAUSTED else EXHAUSTED,
                (actor2_valve, actor2_ttt - 1) if actor2 != EXHAUSTED else EXHAUSTED,
                flow_rate,
                targets,
            )
        )

    return max(options)


targets = tuple(valve for valve in valves if valves[valve][0] > 0)

# try all first targets
best = 0
for idx1 in range(len(targets) - 1):
    for idx2 in range(idx1 + 1, len(targets)):
        best = max(best, maximize(
            26,
            (targets[idx1], distance('AA', targets[idx1])),
            (targets[idx2], distance('AA', targets[idx2])),
            0,
            st(set(targets) - {targets[idx1], targets[idx2]})))
print(best)
