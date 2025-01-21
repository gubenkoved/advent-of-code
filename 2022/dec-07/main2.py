lines = []

with open('data.txt', 'r') as file:
    lines = file.readlines()

# path -> size
files = {}
path = None
idx = 0

while idx < len(lines):
    line = lines[idx]
    line = line.strip()

    if line.startswith('$ cd '):
        arg = line[5:]
        if arg == '/':
            path = '/'
        elif arg == '..':
            path = '/'.join(path.split('/')[:-1])
            if not path:
                path = '/'
        else:
            if not path.endswith('/'):
                path += '/'
            path += arg
        idx += 1
    elif line == '$ ls':
        # read the output while it does not start as a new command
        idx += 1
        while idx < len(lines) and not lines[idx].startswith('$'):
            line = lines[idx].strip()
            if not line.startswith('dir'):
                size, filename = line.split(' ')
                files[path + '/' + filename] = int(size)
            idx += 1


result = None

def traverse(dir_path, threshold):
    global result
    assert dir_path not in files

    subdirs = set()
    for path in files:
        if not path.startswith(dir_path):
            continue
        next_sep_idx = path.find('/', 1 + len(dir_path))
        if next_sep_idx != -1:
            subdirs.add(path[:next_sep_idx])

    for subdir in subdirs:
        traverse(subdir, threshold)

    size = sum(v for k, v in files.items() if k.startswith(dir_path))

    print('dir "%s" total size %d' % (dir_path, size))

    if threshold and size >= threshold:
        if result is None or size < result:
            print('** new best option: "%s" of size %d' % (dir_path, threshold))
            result = size

    return size


used = traverse('/', None)
free = 70000000 - used
required = 30000000 - free

# find the directory which is smallest of ones bigger than or equal to required size
traverse('/', required)
print('required: %d' % required)
print(result)
