import re
import functools

blueprints = []
with open('data.txt', 'r') as file:
    while True:
        line = file.readline()

        if not line:
            break

        match = re.match(
            'Blueprint [0-9]+: Each ore robot costs ([0-9]+) ore. '
            'Each clay robot costs ([0-9]+) ore. '
            'Each obsidian robot costs ([0-9]+) ore and ([0-9]+) clay. '
            'Each geode robot costs ([0-9]+) ore and ([0-9]+) obsidian.',
            line.strip())

        assert match
        blueprints.append((
            int(match.group(1)),  # ore robot cost in ore
            int(match.group(2)),  # clay robot cost in ore
            int(match.group(3)),  # obsidian robot cost in ore
            int(match.group(4)),  # obsidian robot cost in clay
            int(match.group(5)),  # geode robot cost in ore
            int(match.group(6)),  # geode robot cost in obsidian
        ))

# search in the phase space via dynamic programming
@functools.cache
def max_geodes(
        bp, time,
        ore, clay, obsidian, geodes,
        ore_robots, clay_robots, obsidian_robots, geode_robots,
        ore_robots_needed,
) -> int:
    # print('f%s' % ((time, ore, clay, obsidian, geodes, ore_robots, clay_robots, obsidian_robots, geode_robots), ))

    if time == 0:
        return geodes

    # assert ore >= 0
    # assert clay >= 0
    # assert obsidian >= 0
    # assert ore_robots >= 0
    # assert clay_robots >= 0
    # assert obsidian_robots >= 0
    # assert geode_robots >= 0

    # here is the key how to limit search space:
    # first let's assume we need some amount of ore robots (we can enumerate all
    # possible values), then first part of our strategy would be building that
    # amount of ore robots as soon as possible, and only then we would run full
    # search trying all different options;
    # this limits search space enough to calculate the solution timely

    if ore_robots < ore_robots_needed:
        if ore >= bp[0]:
            return max_geodes(
                bp,
                time - 1,
                ore + ore_robots - bp[0],
                clay + clay_robots,
                obsidian + obsidian_robots,
                geodes + geode_robots,
                ore_robots + 1,
                clay_robots,
                obsidian_robots,
                geode_robots,
                ore_robots_needed,
            )
        else:
            return max_geodes(
                bp,
                time - 1,
                ore + ore_robots,
                clay + clay_robots,
                obsidian + obsidian_robots,
                geodes + geode_robots,
                ore_robots,
                clay_robots,
                obsidian_robots,
                geode_robots,
                ore_robots_needed,
            )
    else:
        options = []

        # just time passing by option
        options.append(max_geodes(
            bp,
            time - 1,
            ore + ore_robots,
            clay + clay_robots,
            obsidian + obsidian_robots,
            geodes + geode_robots,
            ore_robots,
            clay_robots,
            obsidian_robots,
            geode_robots,
            ore_robots_needed,
        ))

        # options with building new robots if we can

        # clay robot
        if ore >= bp[1]:
            options.append(max_geodes(
                bp,
                time - 1,
                ore + ore_robots - bp[1],
                clay + clay_robots,
                obsidian + obsidian_robots,
                geodes + geode_robots,
                ore_robots,
                clay_robots + 1,
                obsidian_robots,
                geode_robots,
                ore_robots_needed,
            ))

        # obsidian robot
        if ore >= bp[2] and clay >= bp[3]:
            options.append(max_geodes(
                bp,
                time - 1,
                ore + ore_robots - bp[2],
                clay + clay_robots - bp[3],
                obsidian + obsidian_robots,
                geodes + geode_robots,
                ore_robots,
                clay_robots,
                obsidian_robots + 1,
                geode_robots,
                ore_robots_needed,
            ))

        # geode robot
        if ore >= bp[4] and obsidian >= bp[5]:
            options.append(max_geodes(
                bp,
                time - 1,
                ore + ore_robots - bp[4],
                clay + clay_robots,
                obsidian + obsidian_robots - bp[5],
                geodes + geode_robots,
                ore_robots,
                clay_robots,
                obsidian_robots,
                geode_robots + 1,
                ore_robots_needed,
            ))

        return max(options)


def max_geodes2(bp):
    result = 0
    for ore_robots_needed in range(1, 32):
        print('  assuming ore robots needed is %d' % ore_robots_needed)
        max_geodes.cache_clear()
        cur_count = max_geodes(
            bp,
            32,
            0, 0, 0, 0,
            1, 0, 0, 0,
            ore_robots_needed,
        )
        print('    max geodes is %s' % cur_count)
        result = max(result, cur_count)
    return result


counts = []
for bp_idx, bp in enumerate(blueprints[:3], start=1):
    print('checking blueprint #%d' % bp_idx)
    geodes_count = max_geodes2(bp)
    print('  max count is %d' % geodes_count)
    counts.append(geodes_count)
print(counts)
print(functools.reduce(lambda x, y: x * 1, counts, 1))
