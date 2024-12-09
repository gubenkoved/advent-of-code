file = open('data.txt', 'r')
data = [int(x) for x in file.readline().strip()]

file_sizes = list(enumerate(data[0::2]))
free_sizes = data[1::2]

def enumerate_file_bytes_right():
    for file_id, file_size in reversed(file_sizes):
        for _ in range(file_size):
            yield file_id

total_file_bytes = sum(size for _, size in file_sizes)
expanded_blocks = []
right_iter = enumerate_file_bytes_right()
for (file_id, file_size), free_size in zip(file_sizes, free_sizes):
    for _ in range(file_size):
        expanded_blocks.append(file_id)
        if len(expanded_blocks) == total_file_bytes:
            break
    if len(expanded_blocks) == total_file_bytes:
        break
    # now fill free space
    for _ in range(free_size):
        expanded_blocks.append(next(right_iter))
        if len(expanded_blocks) == total_file_bytes:
            break
    if len(expanded_blocks) == total_file_bytes:
        break

checksum = sum(idx * v for idx, v in enumerate(expanded_blocks))

print(checksum)
