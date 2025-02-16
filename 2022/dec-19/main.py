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
def max_geodes(bp, time, ore, clay, obsidian, geodes, ore_robots, clay_robots, obsidian_robots, geode_robots) -> int:
    # print('f%s' % ((time, ore, clay, obsidian, geodes, ore_robots, clay_robots, obsidian_robots, geode_robots), ))

    if time == 0:
        return geode_robots

    # assert ore >= 0
    # assert clay >= 0
    # assert obsidian >= 0
    # assert ore_robots >= 0
    # assert clay_robots >= 0
    # assert obsidian_robots >= 0
    # assert geode_robots >= 0

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
    ))

    # options with building new robots if we can

    # ore robot
    if ore >= bp[0]:
        options.append(max_geodes(
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
        ))

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
        ))

    return max(options)

total_quality = 0
for bp_idx, bp in enumerate(blueprints, start=1):
    print('checking blueprint #%d' % bp_idx)
    max_geodes.cache_clear()
    total_quality += bp_idx * max_geodes(
        bp,
        24,
        0, 0, 0, 0,
        1, 0, 0, 0,
    )
    print('  total quality is %d' % total_quality)
print(total_quality)
