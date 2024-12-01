if __name__ == '__main__':
    with open('data.txt', 'r') as f:
        time = int(''.join([x for x in f.readline().replace('Time:', '').split(' ') if x]))
        distance = int(''.join([x for x in f.readline().replace('Distance:', '').split(' ') if x]))

    win_ways = 0
    for acceleration_time in range(1, time):
        speed = acceleration_time
        travel_time = time - acceleration_time
        expected_distance = travel_time * speed

        if expected_distance > distance:
            win_ways += 1

    print(win_ways)
