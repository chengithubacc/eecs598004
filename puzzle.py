from tkinter import Frame, Label, CENTER
import tkinter as tk
import random
import logic
import constants as c

def gen():
    return random.randint(0, c.GRID_LEN - 1)

class GameGrid(Frame):
    def __init__(self):
        Frame.__init__(self)

        self.grid()
        self.master.title('2048')
        self.master.bind("<Key>", self.key_down)

        self.commands = {
            c.KEY_UP: logic.up,
            c.KEY_DOWN: logic.down,
            c.KEY_LEFT: logic.left,
            c.KEY_RIGHT: logic.right,
            c.KEY_UP_ALT1: logic.up,
            c.KEY_DOWN_ALT1: logic.down,
            c.KEY_LEFT_ALT1: logic.left,
            c.KEY_RIGHT_ALT1: logic.right,
            c.KEY_UP_ALT2: logic.up,
            c.KEY_DOWN_ALT2: logic.down,
            c.KEY_LEFT_ALT2: logic.left,
            c.KEY_RIGHT_ALT2: logic.right,
        }

        self.grid_cells = []
        self.init_grid()
        self.matrix = logic.new_game(c.GRID_LEN)
        self.history_matrixs = []
        self.update_grid_cells()

        self.mainloop()

    def init_grid(self):
        background = Frame(self, bg=c.BACKGROUND_COLOR_GAME,width=c.SIZE, height=c.SIZE+1)
        background.grid()

        grid_row = []
        cell = Frame(
            background,
            bg=c.BACKGROUND_COLOR_CELL_EMPTY,
            width=c.SIZE,
            height=c.SIZE / c.GRID_LEN
        )
        cell.grid(
            row=0,
            column=0,
            columnspan=4,
            # sticky=tk.E,
            padx=c.GRID_PADDING,
            pady=c.GRID_PADDING
        )
        t = Label(
            master=cell,
            text="Score",
            bg=c.BACKGROUND_COLOR_CELL_EMPTY,
            justify=CENTER,
            font=c.FONT,
            width=22,
            height=2)
        t.grid()
        grid_row.append(t)

        self.grid_cells.append(grid_row)

        for i in range(1,c.GRID_LEN+1):
            grid_row = []
            for j in range(c.GRID_LEN):
                cell = Frame(
                    background,
                    bg=c.BACKGROUND_COLOR_CELL_EMPTY,
                    width=c.SIZE / c.GRID_LEN,
                    height=c.SIZE / c.GRID_LEN
                )
                cell.grid(
                    row=i,
                    column=j,
                    padx=c.GRID_PADDING,
                    pady=c.GRID_PADDING
                )
                t = Label(
                    master=cell,
                    text="",
                    bg=c.BACKGROUND_COLOR_CELL_EMPTY,
                    justify=CENTER,
                    font=c.FONT,
                    width=5,
                    height=2)
                t.grid()
                grid_row.append(t)
            self.grid_cells.append(grid_row)

    def update_grid_layout(self):
        background = Frame(self, bg=c.BACKGROUND_COLOR_GAME,width=c.SIZE, height=c.SIZE+1)
        background.grid()
        grid_row = []
        cell = Frame(
            background,
            bg=c.BACKGROUND_COLOR_CELL_EMPTY,
            width=c.SIZE,
            height=c.SIZE / c.GRID_LEN
        )
        cell.grid(
            row=0,
            column=0,
            columnspan=4,
            # sticky=tk.E,
            padx=c.GRID_PADDING,
            pady=c.GRID_PADDING
        )
        t = Label(
            master=cell,
            text="Score",
            bg=c.BACKGROUND_COLOR_CELL_EMPTY,
            justify=CENTER,
            font=c.FONT,
            width=22,
            height=2)
        t.grid()
        grid_row.append(t)
        self.grid_cells.clear()
        self.grid_cells.append(grid_row)

        for i in range(1,c.GRID_LEN+1):
            grid_row = []
            for j in range(c.GRID_LEN):
                cell = Frame(
                    background,
                    bg=c.BACKGROUND_COLOR_CELL_EMPTY,
                    width=c.SIZE / c.GRID_LEN,
                    height=c.SIZE / c.GRID_LEN
                )
                cell.grid(
                    row=i,
                    column=j,
                    padx=c.GRID_PADDING,
                    pady=c.GRID_PADDING
                )
                t = Label(
                    master=cell,
                    text="",
                    bg=c.BACKGROUND_COLOR_CELL_EMPTY,
                    justify=CENTER,
                    font=c.FONT,
                    width=5,
                    height=2)
                t.grid()
                grid_row.append(t)
            self.grid_cells.append(grid_row)

    def update_grid_cells(self):
        score = 0
        max_num = 0
        max_color_b = None
        max_color_f = None
        for i in range(0,c.GRID_LEN):
            for j in range(c.GRID_LEN):
                #print(i,j,len(self.matrix[i]))
                new_number = self.matrix[i][j]
                if new_number == 0:
                    self.grid_cells[i+1][j].configure(text="",bg=c.BACKGROUND_COLOR_CELL_EMPTY)
                else:
                    self.grid_cells[i+1][j].configure(
                        text=str(new_number),
                        bg=c.BACKGROUND_COLOR_DICT[new_number],
                        fg=c.CELL_COLOR_DICT[new_number]
                    )
                    score += new_number
                    if (new_number > max_num):
                        max_num = new_number
                        max_color_b = c.BACKGROUND_COLOR_DICT[new_number]
                        max_color_f = c.CELL_COLOR_DICT[new_number]
        self.grid_cells[0][0].configure(
            text="Score: "+str(score),
            bg=max_color_b,
            fg=max_color_f
        )
        self.update_idletasks()

    def key_down(self, event):
        key = event.keysym
        print(event)
        if key == c.KEY_QUIT: exit()
        if key == c.KEY_CHANGE:
            color_list = list(c.BACKGROUND_COLOR_DICT.values())
            print(color_list)
            random.shuffle(color_list)
            for num, color in zip(c.BACKGROUND_COLOR_DICT.keys(), color_list):
                c.BACKGROUND_COLOR_DICT[num] = color
            self.update_grid_cells()

        elif key == c.KEY_RESET:
            c.BACKGROUND_COLOR_DICT = c.BACKGROUND_COLOR_DICT_ORG.copy()
            self.update_grid_cells()
            # changed to expand grid size
            print("Reset Triggered")
            self.matrix = logic.expand_size(self.matrix)
            self.update_grid_layout()
            self.update_grid_cells()
            print(len(self.matrix), c.GRID_LEN)

        if key == c.KEY_BACK and len(self.history_matrixs) > 1:
            self.matrix = self.history_matrixs.pop()
            self.update_grid_cells()
            print('back on step total step:', len(self.history_matrixs))
        elif key in self.commands:
            self.matrix, done = self.commands[key](self.matrix)
            if done:
                self.matrix = logic.add_two(self.matrix)
                # record last move
                self.history_matrixs.append(self.matrix)
                self.update_grid_cells()
                if logic.game_state(self.matrix) == 'win':
                    self.grid_cells[1][1].configure(text="You", bg=c.BACKGROUND_COLOR_CELL_EMPTY)
                    self.grid_cells[1][2].configure(text="Win!", bg=c.BACKGROUND_COLOR_CELL_EMPTY)
                if logic.game_state(self.matrix) == 'lose':
                    self.grid_cells[1][1].configure(text="You", bg=c.BACKGROUND_COLOR_CELL_EMPTY)
                    self.grid_cells[1][2].configure(text="Lose!", bg=c.BACKGROUND_COLOR_CELL_EMPTY)

    # def generate_next(self):
    #     index = (gen(), gen())
    #     while self.matrix[index[0]][index[1]] != 0:
    #         index = (gen(), gen())
    #     self.matrix[index[0]][index[1]] = 2
if __name__ == '__main__':
    game_grid = GameGrid()