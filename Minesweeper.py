import numpy as np
import tkinter as tk
from math import *
import time

flagcount = 0
is_win = None


def main():

    global flagcount
    flagcount = 0
    global is_win
    is_win = None


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

    def run(x, y, density, run_button):
        x = int(x.get())
        y = int(y.get())
        density = float(density.get()) / 100
        area = x * y
        if density >= 1:
            root.destroy()
            main()

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

        flag_limit = ceil(minecount * .85)

        # proximity test
        for mine in Mine._registry:
            for i in [mine.i - 1, mine.i, mine.i + 1]:
                if i < 0 or i > y - 1:
                    continue
                for j in [mine.j - 1, mine.j, mine.j + 1]:
                    if j < 0 or j > x - 1:
                        continue
                    if type(grid[i, j]) != Mine:
                        grid[i, j] += 1

        display = grid.copy()
        display = display.astype('S')

        for mine in Mine._registry:
            display[mine.i, mine.j] = mine.symbol
        display[np.where(display == b'0')] = b' '

        # switch from setup to game
        info1.destroy()
        info2.destroy()
        info3.destroy()
        x_selection.destroy()
        y_selection.destroy()
        density_selection.destroy()
        run_button.destroy()
        root.geometry(f'{43 * x}x{40 * y + 57}')

        # colors of revealed text
        colors = {b'1': 'blue',
                  b'2': 'green',
                  b'3': 'red',
                  b'4': '#4B0082',
                  b'5': 'orange',
                  b'6': '#ff00ff',
                  b'7': '#ff00ff',
                  b'8': '#ff00ff'}

        clicked_tiles = np.zeros(shape=(y, x))
        tiles = np.ndarray(shape=(y, x), dtype='O')

        # flag_counter = tk.Label(root, text=f'0/{flag_limit}')
        # flag_counter.grid(row=y)

        def foo():
            pass

        def toggle_flag(pos):
            global flagcount
            if is_win == None:
                if tiles[pos[0], pos[1]]['text'] == '':  # and flagcount < flag_limit:
                    tiles[pos[0], pos[1]]['text'] = '!'
                    flagcount += 1
                    # flag_counter['text'] = f'{flagcount}/{flag_limit}'
                elif tiles[pos[0], pos[1]]['text'] == '!':
                    tiles[pos[0], pos[1]]['text'] = ''
                    flagcount -= 1
                    # flag_counter['text'] = f'{flagcount}/{flag_limit}'

        def replay():
            root.destroy()
            main()

        def lose():
            msg = tk.Label(root, text='Game Over', fg='red', font='boldFont')
            msg.grid(row=y, columnspan=x)
            for pos, reveal_text in np.ndenumerate(display):
                target = tiles[pos[0], pos[1]]
                target['text'] = reveal_text
                target['relief'] = 'sunken'
                target['fg'] = colors.get(reveal_text, None)
                target['bg'] = '#ddd'
                target['font'] = 'boldFont'
                target.config(command=lambda: foo())
            replay_button = tk.Button(root, text='Play Again', command=lambda: replay())
            replay_button.grid(row=y + 1, columnspan=x)
            global is_win
            is_win = False

        def win():
            for pos, tile in np.ndenumerate(display):
                tiles[pos[0], pos[1]].config(command=lambda: foo())
            msg = tk.Label(root, text='Clear', fg='green', font='boldFont')
            msg.grid(row=y, columnspan=x)
            replay_button = tk.Button(root, text='Play Again', command=lambda: replay())
            replay_button.grid(row=y + 1, columnspan=x)
            global is_win
            is_win = True

        def show(pos, text):
            target = tiles[pos[0], pos[1]]
            target['text'] = text
            target['relief'] = 'sunken'
            target['fg'] = colors.get(text, None)
            target['bg'] = '#ddd'
            target['font'] = 'boldFont'
            if text == b'X' and is_win == None:  # losing condition
                lose()
                target['bg'] = 'red'
            elif is_win == None:  # count tile as clicked
                clicked_tiles[pos[0], pos[1]] = 1
                if np.sum(clicked_tiles) == area - minecount:  # winning condition
                    win()
            if text == b' ':  # show islands of blank tiles and their borders
                for i in [pos[0] - 1, pos[0], pos[0] + 1]:
                    if i < 0 or i > y - 1:
                        continue
                    for j in [pos[1] - 1, pos[1], pos[1] + 1]:
                        if j < 0 or j > x - 1:
                            continue
                        elif clicked_tiles[i, j] != 1:
                            show((i, j), display[i, j])

        def create_tile(pos, text):
            tile = tk.Button(root, command=lambda: show(pos, text), font='boldFont')
            tile.config(width=3, height=1)
            tile.grid(row=pos[0], column=pos[1])
            tile.bind('<Button-3>', lambda x: toggle_flag(pos))
            tiles[pos[0], pos[1]] = tile

        for pos, text in np.ndenumerate(display):
            create_tile((pos[0], pos[1]), text)

    run_button = tk.Button(root, text='Go', command=lambda: run(x_selection, y_selection, density_selection, run_button))
    run_button.grid(row=3, columnspan=2, ipadx=20)

    root.mainloop()


main()

'''
ideas to implement:
assign icons to the mines/flags
timer
'''
