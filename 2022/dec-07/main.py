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


size_at_most_threshold = 0

def traverse(dir_path):
    global size_at_most_threshold
    assert dir_path not in files

    subdirs = set()
    for path in files:
        if not path.startswith(dir_path):
            continue
        next_sep_idx = path.find('/', 1 + len(dir_path))
        if next_sep_idx != -1:
            subdirs.add(path[:next_sep_idx])

    for subdir in subdirs:
        traverse(subdir)

    size = sum(v for k, v in files.items() if k.startswith(dir_path))

    print('dir "%s" total size %d' % (dir_path, size))

    if size <= 100000:
        size_at_most_threshold += size
        print(' ** below threshold!')

    return size


traverse('/')
print(size_at_most_threshold)
