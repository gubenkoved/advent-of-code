file = open('data.txt', 'r')
data = [int(x) for x in file.readline().strip()]

file_sizes = list(enumerate(data[0::2]))
free_sizes = data[1::2]

layout = []

for (file_id, file_size), free_size in zip(file_sizes, free_sizes):
    layout.append((file_id, file_size))
    layout.append((-1, free_size))

# defragmentation pass
for file_id, file_size in reversed(file_sizes):
    # find free left-most spot that fits
    for idx in range(len(layout)):
        if layout[idx][0] == -1 and layout[idx][1] >= file_size:
            # move the file!
            leftover_space = layout[idx][1] - file_size
            layout[idx] = (file_id, file_size)
            layout.insert(idx + 1, (-1, leftover_space))
            break

# now create expanded view and do not include the files twice (it means there was a move left)
seen = set()
expanded = []
for file_id, size in layout:
    if file_id != -1:
        if file_id not in seen:
            seen.add(file_id)
            expanded.extend([file_id] * size)
        else:
            # file was moved, so this is a free space now
            expanded.extend([0] * size)
    else:
        expanded.extend([0] * size)

checksum = sum(idx * v for idx, v in enumerate(expanded))

print(checksum)
