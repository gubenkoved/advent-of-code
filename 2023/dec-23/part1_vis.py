import sys
from tkinter import *

from part1 import read_field, walk


def draw_cell(cell, color):
    row, col = cell
    x, y = col * cell_size, row * cell_size
    x2, y2 = x + cell_size, y + cell_size

    # x += 1; y += 1
    # x2 -= 1; y2 -= 1
    # canvas.create_rectangle(x, y, x2, y2, fill=color, outline='')
    canvas.create_oval(x, y, x2, y2, fill=color, outline='')


def draw_field():
    for row in range(rows):
        for col in range(cols):

            if field[row][col] == '#':
                draw_cell((row, col), 'gray')
            # elif field[row][col] in '<>v^':
            #     x, y = col * cell_size, row * cell_size
            #     canvas.create_text(
            #         x + cell_size // 2, y + cell_size // 2, text=field[row][col],
            #         font='"Ubuntu Mono" 10 bold', fill='gray')


def draw_solution():

    last_visited = set()

    def on_step(cur, visited):
        nonlocal last_visited

        # rollbacks
        to_clean = last_visited - visited
        for clean_cell in to_clean:
            draw_cell(clean_cell, 'yellow')

        last_visited = set(visited)

        draw_cell(cur, 'red')

        # force redraw canvas w/o giving up control flow
        root.update()

    walk(
        field,
        cur=(0, 1),
        constraint='',
        visited=set(),
        on_step_fn=on_step,
    )


if __name__ == '__main__':
    field = read_field()
    rows, cols = len(field), len(field[0])
    cell_size = 8

    width, height = cols * cell_size, rows * cell_size

    root = Tk()
    root.geometry("%dx%d" % (width, height))

    canvas = Canvas(root, bg='white', height=height, width=width)
    redraw_counter = 0

    canvas.pack()

    draw_field()

    sys.setrecursionlimit(1000000)

    root.after(3000, draw_solution)
    root.mainloop()
