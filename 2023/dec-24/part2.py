import sympy

data = []

with open('input.txt', 'r') as f:
    while True:
        line = f.readline()
        if not line:
            break
        pos, speed = line.strip().split('@')
        data.append((
            tuple(int(x) for x in pos.split(',')),
            tuple(int(x) for x in speed.split(',')),
        ))

x, y, z = sympy.symbols('x, y, z')
vx, vy, vz = sympy.symbols('vx, vy, vz')

(x1, y1, z1), (vx1, vy1, vz1) = data[0]
(x2, y2, z2), (vx2, vy2, vz2) = data[1]
(x3, y3, z3), (vx3, vy3, vz3) = data[2]

result = sympy.solve([
    (x - x1) / (vx1 - vx) - (y - y1)/(vy1 - vy),
    (x - x1) / (vx1 - vx) - (z - z1)/(vz1 - vz),
    (x - x2) / (vx2 - vx) - (y - y2)/(vy2 - vy),
    (x - x2) / (vx2 - vx) - (z - z2)/(vz2 - vz),
    (x - x3) / (vx3 - vx) - (y - y3)/(vy3 - vy),
    (x - x3) / (vx3 - vx) - (z - z3)/(vz3 - vz),
], [x, y, z, vx, vy, vz])

result = result[0]
print(int(sum(result[:3])))
