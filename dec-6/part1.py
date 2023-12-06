if __name__ == '__main__':
    with open('data.txt', 'r') as f:
        times = [int(x) for x in f.readline().replace('Time:', '').split(' ') if x]
        distances = [int(x) for x in f.readline().replace('Distance:', '').split(' ') if x]

    result = 1

    for idx in range(len(times)):

        win_ways = 0
        for acceleration_time in range(1, times[idx]):
            speed = acceleration_time
            travel_time = times[idx] - acceleration_time
            expected_distance = travel_time * speed

            if expected_distance > distances[idx]:
                win_ways += 1

        result *= win_ways

    print(result)