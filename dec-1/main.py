if __name__ == '__main__':
    result = 0
    with open('data.txt') as f:
        while True:
            line = f.readline()

            replacements = {
                'one': '1',
                'two': '2',
                'three': '3',
                'four': '4',
                'five': '5',
                'six': '6',
                'seven': '7',
                'eight': '8',
                'nine': '9',
            }

            if not line:
                break

            numbers = []
            buffer = ''
            for c in line:
                if c >= '0' and c <= '9':
                    numbers.append(c)
                    buffer = ''
                else:
                    buffer += c

                    matched = False
                    for k, v in replacements.items():
                        if buffer[-len(k):] == k:
                            numbers.append(v)
                            matched = True
                            break

                    # if matched:
                    #     buffer = ''

            num = int(numbers[0] + numbers[-1])
            result += num

            print('%s -> %s -> %s' % (line.strip(), numbers, num))

    print(result)
