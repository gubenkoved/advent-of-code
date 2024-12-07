file = open('data.txt', 'r')

rules = []

for line in file.readlines():
    total, numbers = line.split(':')
    total = int(total)
    numbers = [int(x) for x in numbers.strip().split(' ')]
    rules.append((total, numbers))


def can_be_combined_into(result, cur_result, right_numbers):
    if not right_numbers:
        return result == cur_result
    return (can_be_combined_into(result, cur_result + right_numbers[0], right_numbers[1:]) or
            can_be_combined_into(result, cur_result * right_numbers[0], right_numbers[1:]) or
            can_be_combined_into(result, int(str(cur_result) + str(right_numbers[0])), right_numbers[1:]))


result = 0
for total, numbers in rules:
    if can_be_combined_into(total, numbers[0], numbers[1:]):
        result += total
print(result)
