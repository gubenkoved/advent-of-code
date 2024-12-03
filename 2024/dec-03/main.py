import re

file = open('data.txt', 'r')
data = file.read()

result = 0
for match in re.finditer('mul\(([0-9]{1,3}),([0-9]{1,3})\)', data):
    result += int(match.group(1)) * int(match.group(2))
print(result)

result = 0
enabled = True
for match in re.finditer('(mul\(([0-9]{1,3}),([0-9]{1,3})\))|(do\(\))|(don\'t\(\))', data):
    if match.group(0) == 'do()':
        enabled = True
    elif match.group(0) == 'don\'t()':
        enabled = False
    else:
        if enabled:
            result += int(match.group(2)) * int(match.group(3))
print(result)