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

        return mapping

    with open('data.txt', 'r') as f:
        line = f.readline()

        seeds = [int(x) for x in line.replace('seeds: ', '').split(' ')]
        seed_to_soil = read_mapping(f)
        soil_to_fertilizer = read_mapping(f)
        fertilizer_to_water = read_mapping(f)
        water_to_light = read_mapping(f)
        light_to_temperature = read_mapping(f)
        temperature_to_humidity = read_mapping(f)
        humidity_to_location = read_mapping(f)

    def map_generic(mapping, source_value):
        for dest, source, length in mapping:
            if source_value >= source and source_value < source + length:
                delta = source_value - source
                return dest + delta
        # not re-mapped
        return source_value

    def soil(seed):
        return map_generic(seed_to_soil, seed)

    def fertilizer(soil):
        return map_generic(soil_to_fertilizer, soil)

    def water(fertilizer):
        return map_generic(fertilizer_to_water, fertilizer)

    def light(water):
        return map_generic(water_to_light, water)

    def temperature(light):
        return map_generic(light_to_temperature, light)

    def humidity(temperature):
        return map_generic(temperature_to_humidity, temperature)

    def location(humidity):
        return map_generic(humidity_to_location, humidity)

    soils = [soil(x) for x in seeds]
    fertilizers = [fertilizer(x) for x in soils]
    waters = [water(x) for x in fertilizers]
    lights = [light(x) for x in waters]
    temperatures = [temperature(x) for x in lights]
    humidities = [humidity(x) for x in temperatures]
    locations = [location(x) for x in humidities]

    print(min(locations))
