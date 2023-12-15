if __name__ == '__main__':
    steps = []
    with open('data.txt', 'r') as f:
        line = f.readline().strip('\n')
        steps = line.split(',')

    def my_hash(s):
        result = 0
        for c in s:
            result += ord(c)
            result *= 17
            result %= 256
        return result

    print(sum(my_hash(s) for s in steps))
