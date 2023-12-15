if __name__ == '__main__':
    steps = []
    with open('data.txt', 'r') as f:
        line = f.readline().strip('\n')
        steps = line.split(',')

    # split label and operation
    stage2 = []
    for step in steps:
        if step.endswith('-'):
            stage2.append((step[:-1], '-'))
        elif step[-2] == '=':
            stage2.append((step[:-2], step[-2:]))
        else:
            stage2.append((step[:-2], ''))

    def my_hash(s):
        result = 0
        for c in s:
            result += ord(c)
            result *= 17
            result %= 256
        return result

    boxes = [[] for _ in range(256)]
    for label, operation in stage2:
        box_idx = my_hash(label)
        box = boxes[box_idx]
        if operation.startswith('='):
            power = int(operation[1])
            for lens_idx in range(len(boxes[box_idx])):
                if box[lens_idx][0] == label:
                    box[lens_idx] = (label, power)
                    break
            else:
                box.append((label, power))
        elif operation.endswith('-'):
            for lens_idx in range(len(boxes[box_idx])):
                if box[lens_idx][0] == label:
                    box.pop(lens_idx)
                    break

    result = 0
    for box_idx in range(len(boxes)):
        box = boxes[box_idx]
        for lens_idx in range(len(box)):
            result += (box_idx + 1) * (lens_idx + 1) * box[lens_idx][1]
    print(result)
