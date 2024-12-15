import os
import re
from collections import defaultdict
import zlib
import plotly.express as px


file = open('data.txt', 'r')


robots = []

# p=99,52 v=42,38
for line in file:
    m = re.match('p=([0-9]+),([0-9]+) v=(-?[0-9]+),(-?[0-9]+)', line.strip())
    assert m
    robots.append((
        # position
        (int(m.group(1)), int(m.group(2))),
        # velocity
        (int(m.group(3)), int(m.group(4))),
    ))

width, height = 101, 103

def simulate(pos, vel, rounds):
    return (
        (pos[0] + vel[0] * rounds) % width,
        (pos[1] + vel[1] * rounds) % height,
    )


def quadrant_id(position):
    mid_w = width // 2
    mid_h = height // 2

    if position[0] == mid_w or position[1] == mid_h:
        return None

    return (
        (position[0] < mid_w),
        (position[1] < mid_h),
    )


def field_to_string(positions):
    positions_map = defaultdict(int)
    for position in positions:
        positions_map[position] += 1
    result = ''
    for row in range(height):
        for col in range(width):
            if (col, row) not in positions_map:
                result += '.'
            else:
                result += str(positions_map[(col, row)])
        result += '\n'
    return result


# the whole thing loops every 103*101 (see Chinese reminders theorem), so we only need
# 103 * 101 states, then among them we need states which have the biggest order or
# lowest entropy, which can be estimated simply by compression algorithm because
# randomness does not compress!


def compressed_size(str):
    return len(zlib.compress(str.encode()))

compressed_sizes = []

for round_idx in range(103 * 101):
    print('round #%d' % round_idx)
    positions = [simulate(robot[0], robot[1], round_idx) for robot in robots]
    field_str = field_to_string(positions)
    compressed_sizes.append((round_idx, compressed_size(field_str), field_str))

# fields by compressed size ascending
compressed_sizes.sort(key=lambda x: x[1])
os.makedirs('fields', exist_ok=True)

for idx in range(100):
    round_idx, compressed_size, field_str = compressed_sizes[idx]
    print('round %6d, compressed size: %d' % (round_idx, compressed_size))
    with open('fields/%03d_field_%d.txt' % (idx, round_idx), 'w') as f:
        f.write(field_str)


def nicer_layout(fig):
    fig.update_layout(
        template='seaborn',
        font=dict(
            family='Ubuntu Mono'
        ),
        paper_bgcolor='white',
        plot_bgcolor='white',
        xaxis=dict(
            showgrid=True,
            gridcolor='#e3e3e3',
            gridwidth=1,
            griddash='dot',
            nticks=16*3,
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor='#e3e3e3',
            gridwidth=1,
            griddash='dot',
            nticks=9*4,
        )
    )

fig = px.histogram(
    x=[data[1] for data in compressed_sizes],
    nbins=200,
    log_y=True,
)
fig.update_layout(
    xaxis=dict(
        title='Compressed size',
    )
)
nicer_layout(fig)
fig.write_html('histogram.html')

# round idx vs size

fig = px.scatter(
    x=[data[0] for data in compressed_sizes],
    y=[data[1] for data in compressed_sizes],
)
fig.update_traces(
    marker=dict(
        size=6,
        opacity=0.5,
        color='#d4362a',
    )
)
fig.update_layout(
    xaxis=dict(
        title='Round index',
    ),
    yaxis=dict(
        title='Compressed size',
    )
)
nicer_layout(fig)
fig.write_html('scatter.html')
