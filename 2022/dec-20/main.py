nums = []

with open('data.txt', 'r') as f:
    for line in f:
        nums.append(int(line))


class Node:
    def __init__(self, value):
        self.value = value
        self.prev = None
        self.next = None

    def __repr__(self):
        return f'Node({self.value})'


# construct the linked list from the numbers
head = Node(nums[0])
cur = head
zero_node = None

# capture the original order as we will be moving it using orig order
orig_order = [cur]

for num in nums[1:]:
    node = Node(num)
    cur.next = node
    node.prev = cur
    cur = node

    orig_order.append(node)

    if num == 0:
        assert zero_node is None
        zero_node = node

# make it cyclic
cur.next = head
head.prev = cur


# move(a, +2)
# x a b c d e
#   ^
# x b c a d e

def move(node, delta):
    if delta == 0:
        return

    # find the target left and right pointers between which we need to
    # insert the number
    if delta > 0:
        left = node
        for _ in range(delta):
            left = left.next
        right = left.next
    else:
        right = node
        for _ in range(abs(delta)):
            right = right.prev
        left = right.prev

    # take the node out
    node.prev.next = node.next
    node.next.prev = node.prev

    # insert into the new location
    node.next = right
    node.prev = left

    left.next = node
    right.prev = node


def print_all(start_node):
    nums = []
    cur = start_node
    while True:
        nums.append(cur.value)
        cur = cur.next
        if cur is start_node:
            break
    print(nums)

# print initial disposition
print_all(head)

for node in orig_order:
    move(node, delta=node.value)

def find_at(node, delta):
    cur = node
    for _ in range(abs(delta)):
        if delta > 0:
            cur = cur.next
        else:
            cur = cur.prev
    return cur


print_all(zero_node)

print(sum([
    find_at(zero_node, +1000).value,
    find_at(zero_node, +2000).value,
    find_at(zero_node, +3000).value,
]))
