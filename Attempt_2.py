import numpy as np
import tkinter as tk

root = tk.Tk()
root.title('Minesweeper')
root.geometry('200x100')

x_selection = tk.Entry(root, textvariable=tk.IntVar())
y_selection = tk.Entry(root, textvariable=tk.IntVar())
density_selection = tk.Entry(root, textvariable=tk.IntVar())
info1 = tk.Label(root, text='Width:')
info2 = tk.Label(root, text='Height:')
info3 = tk.Label(root, text='% Mines:')

info1.grid()
info2.grid(column=0, row=1)
info3.grid(column=0, row=2)
x_selection.grid(column=1, row=0)
y_selection.grid(column=1, row=1)
density_selection.grid(column=1, row=2)


def run(x, y, density):
    x = int(x.get())
    y = int(y.get())
    density = float(density.get())
    area = x * y
    # need better exception handling for >100% mines
    if density >= 1:
        exit()

    class Mine:
        _registry = []

        def __init__(self, pos):
            self.pos = pos
            self.i = pos[0]
            self.j = pos[1]
            self.symbol = 'X'
            Mine._registry.append(self)

    grid = np.zeros(shape=(y, x), dtype='O')

    # distributing mines
    minecount = 0
    while minecount != round(density * area):
        i = np.random.randint(0, y)  # rows
        j = np.random.randint(0, x)  # columns
        if type(grid[i, j]) != Mine:
            grid[i, j] = Mine((i, j))
            minecount += 1

    # proximity test
    for mine in Mine._registry:
        # check if pos is 0, x, or y
        if mine.i == 0:  # top row
            if type(grid[mine.i + 1, mine.j]) == int:
                grid[mine.i + 1, mine.j] += 1  # down
            if mine.j != x - 1:  # not last column
                if type(grid[mine.i + 1, mine.j + 1]) == int:
                    grid[mine.i + 1, mine.j + 1] += 1  # down right
                if type(grid[mine.i, mine.j + 1]) == int:
                    grid[mine.i, mine.j + 1] += 1  # right
            if mine.j != 0:  # not first column
                if type(grid[mine.i + 1, mine.j - 1]) == int:
                    grid[mine.i + 1, mine.j - 1] += 1  # down left
                if type(grid[mine.i, mine.j - 1]) == int:
                    grid[mine.i, mine.j - 1] += 1  # left

        elif mine.i == y - 1:  # bottom row
            if type(grid[mine.i - 1, mine.j]) == int:
                grid[mine.i - 1, mine.j] += 1  # up
            if mine.j != x - 1:  # not last column
                if type(grid[mine.i - 1, mine.j + 1]) == int:
                    grid[mine.i - 1, mine.j + 1] += 1  # up right
                if type(grid[mine.i, mine.j + 1]) == int:
                    grid[mine.i, mine.j + 1] += 1  # right
            if mine.j != 0:  # not first column
                if type(grid[mine.i - 1, mine.j - 1]) == int:
                    grid[mine.i - 1, mine.j - 1] += 1  # up left
                if type(grid[mine.i, mine.j - 1]) == int:
                    grid[mine.i, mine.j - 1] += 1  # left

        elif mine.j == 0 and 0 < mine.i < y - 1:  # first column between top and bottom rows
            if type(grid[mine.i, mine.j + 1]) == int:
                grid[mine.i, mine.j + 1] += 1  # right
            if type(grid[mine.i + 1, mine.j]) == int:
                grid[mine.i + 1, mine.j] += 1  # down
            if type(grid[mine.i - 1, mine.j]) == int:
                grid[mine.i - 1, mine.j] += 1  # up
            if type(grid[mine.i + 1, mine.j + 1]) == int:
                grid[mine.i + 1, mine.j + 1] += 1  # down right
            if type(grid[mine.i - 1, mine.j + 1]) == int:
                grid[mine.i - 1, mine.j + 1] += 1  # up right

        elif mine.j == x - 1 and 0 < mine.i < y - 1:  # last column between top and bottom rows
            if type(grid[mine.i, mine.j - 1]) == int:
                grid[mine.i, mine.j - 1] += 1  # left
            if type(grid[mine.i + 1, mine.j]) == int:
                grid[mine.i + 1, mine.j] += 1  # down
            if type(grid[mine.i - 1, mine.j]) == int:
                grid[mine.i - 1, mine.j] += 1  # up
            if type(grid[mine.i + 1, mine.j - 1]) == int:
                grid[mine.i + 1, mine.j - 1] += 1  # down left
            if type(grid[mine.i - 1, mine.j - 1]) == int:
                grid[mine.i - 1, mine.j - 1] += 1  # up left

        else:  # middle
            if type(grid[mine.i, mine.j - 1]) == int:
                grid[mine.i, mine.j - 1] += 1  # left
            if type(grid[mine.i, mine.j + 1]) == int:
                grid[mine.i, mine.j + 1] += 1  # right
            if type(grid[mine.i + 1, mine.j]) == int:
                grid[mine.i + 1, mine.j] += 1  # down
            if type(grid[mine.i - 1, mine.j]) == int:
                grid[mine.i - 1, mine.j] += 1  # up
            if type(grid[mine.i + 1, mine.j - 1]) == int:
                grid[mine.i + 1, mine.j - 1] += 1  # down left
            if type(grid[mine.i - 1, mine.j - 1]) == int:
                grid[mine.i - 1, mine.j - 1] += 1  # up left
            if type(grid[mine.i + 1, mine.j + 1]) == int:
                grid[mine.i + 1, mine.j + 1] += 1  # down right
            if type(grid[mine.i - 1, mine.j + 1]) == int:
                grid[mine.i - 1, mine.j + 1] += 1  # up right

    display = grid.copy()
    display = display.astype('S')

    for mine in Mine._registry:
        display[mine.i, mine.j] = mine.symbol
    display[np.where(display == b'0')] = b' '

    # switch windows
    root.destroy()
    root2 = tk.Tk()
    root2.title('Minesweeper')

    colors = {b'1': 'blue',
              b'2': 'green',
              b'3': 'red',
              b'4': 'purple',
              b'5': 'orange',
              b'6': 'yellow',
              b'7': 'yellow',
              b'8': 'yellow'}

    clicked_tiles = np.zeros(shape=(y, x))
    tiles = np.ndarray(shape=(y, x), dtype='O')

    def toggle_flag(pos, text):
        if tiles[pos[0], pos[1]]['text'] == '':
            tiles[pos[0], pos[1]]['text'] = '!'
        else:
            tiles[pos[0], pos[1]]['text'] = ''

    def lose():
        msg = tk.Label(root2, text='Game Over', fg='red', font='boldFont')
        msg.grid(row=y, columnspan=x)
        n = -1
        # show all tiles
        for i in display:
            n += 1
            m = -1
            for reveal_text in i:
                m += 1
                target = tiles[n, m]
                target['text'] = reveal_text
                target['relief'] = 'sunken'
                target['fg'] = colors.get(reveal_text, None)
                target['bg'] = '#ddd'
                target['font'] = 'boldFont'

    def win():
        msg = tk.Label(root2, text='Clear', fg='green', font='boldFont')
        msg.grid(row=y, columnspan=x)

    def show(pos, text):
        target = tiles[pos[0], pos[1]]
        target['text'] = text
        target['relief'] = 'sunken'
        target['fg'] = colors.get(text, None)
        target['bg'] = '#ddd'
        target['font'] = 'boldFont'
        if text == b'X':  # losing condition
            lose()
        else:  # count tile as clicked
            clicked_tiles[pos[0], pos[1]] = 1
            if sum(sum(clicked_tiles)) == area - minecount:  # winning condition
                win()

    def create_tile(pos, text):
        tile = tk.Button(root2, command=lambda: show(pos, text), font='boldFont')
        tile.config(width=3, height=1)
        tile.grid(row=pos[0], column=pos[1])
        tile.bind('<Button-3>', lambda x: toggle_flag(pos, text))
        tiles[pos[0], pos[1]] = tile

    n = -1
    for i in display:
        n += 1
        m = -1
        for tile in i:
            m += 1
            create_tile((n, m), tile)


run_button = tk.Button(root, text='Go', command=lambda: run(x_selection, y_selection, density_selection))
run_button.grid(row=3, columnspan=2, ipadx=20)

root.mainloop()

# assign icons to the mines/flags
# distribute mines after click so first click won't be a mine
# show contiguous 0's when one is clicked
# lock in win condition
