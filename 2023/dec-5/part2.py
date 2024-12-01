import itertools

if __name__ == '__main__':
    def read_mapping(f):
        # find start
        while True:
            line = f.readline()
            if line.endswith('map:\n'):
                break

        # dest, source, len
        mapping = []

        # read mapping
        while True:
            line = f.readline()

            if not line.strip():
                break

            dest, source, len = line.split(' ')
            mapping.append(
                (int(dest), int(source), int(len))
            )

        # sort mapping by increasing of the source
        mapping.sort(key=lambda t: t[1])

        return mapping

    with open('data.txt', 'r') as f:
        line = f.readline()

        seeds_raw = [int(x) for x in line.replace('seeds: ', '').split(' ')]

        # convert to ranges
        seeds = []
        for idx in range(0, len(seeds_raw), 2):
            # seeds are (start, len)
            seeds.append((seeds_raw[idx], seeds_raw[idx] + seeds_raw[idx + 1]))

        seed_to_soil = read_mapping(f)
        soil_to_fertilizer = read_mapping(f)
        fertilizer_to_water = read_mapping(f)
        water_to_light = read_mapping(f)
        light_to_temperature = read_mapping(f)
        temperature_to_humidity = read_mapping(f)
        humidity_to_location = read_mapping(f)

    # takes mapping and single source range and returns one or more
    # destination ranges after the mapping
    def map_range(mapping, in_source_range):
        dest_ranges = []

        # start with source range start
        ptr = in_source_range[0]

        for dest_begin, source_begin, length in mapping:
            source_end = source_begin + length - 1

            # no intersection
            if source_end <= ptr:
                continue

            if source_begin > in_source_range[1]:
                continue

            mapped_start = max(source_begin, ptr)

            if mapped_start > ptr:
                # mark part [ptr, mapped_start - 1] as mapped 1-to-1
                dest_ranges.append(
                    (ptr, mapped_start - 1)
                )

            mapped_end = min(source_end, in_source_range[1])

            # map the range
            delta = dest_begin - source_begin
            dest_ranges.append(
                (mapped_start + delta, mapped_end + delta)
            )

            ptr = mapped_end + 1

        # map the end part if needed
        if ptr < in_source_range[1]:
            dest_ranges.append(
                (ptr, in_source_range[1])
            )

        return dest_ranges

    def transform(mapping, source_ranges):
        return list(itertools.chain(*[map_range(mapping, x) for x in source_ranges]))

    ranges = seeds
    ranges = transform(seed_to_soil, ranges)
    ranges = transform(soil_to_fertilizer, ranges)
    ranges = transform(fertilizer_to_water, ranges)
    ranges = transform(water_to_light, ranges)
    ranges = transform(light_to_temperature, ranges)
    ranges = transform(temperature_to_humidity, ranges)
    ranges = transform(humidity_to_location, ranges)

    # min of start of the ranges
    print(min(r[0] for r in ranges))
