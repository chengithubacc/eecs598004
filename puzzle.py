import threading
import time
from tkinter import Frame, Label, CENTER
import tkinter as tk
import random
import logic
import constants as c
from PIL import ImageTk, Image

def gen():
    return random.randint(0, c.GRID_LEN - 1)

class GameGrid(Frame):
    def __init__(self):
        Frame.__init__(self)
        # self.root = tk.Tk()

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
        path = "images/block2.png"
        image = Image.open(path)
        self.raw_image = Image.open(path)
        image.putalpha(0)  # Half alpha; alpha argument must be an int
        image = image.resize((c.SIZE, c.SIZE), Image.ANTIALIAS)
        self.blockImg = ImageTk.PhotoImage(image)
        # self.blockImg = ImageTk.PhotoImage(image)

        self.lastInput = time.time()
        self.frozen_flag = False


        import cv2
        #
        img = cv2.imread("images/block2.png")
        # print(img)
        self.bgra = cv2.cvtColor(img, cv2.COLOR_BGR2BGRA)
        #
        # # Set alpha layer semi-transparent with Numpy indexing, B=0, G=1, R=2, A=3
        self.bgra[..., 3] = 50
        self.blockImg2 = Image.fromarray(self.bgra)

        # Save result
        # cv2.imwrite('result.png', bgra)
        # print(img[100][50])


        # test = ImageTk.PhotoImage(image1)
        # label1 = tk.Label(image=self.blockImg)
        # label1.image = self.blockImg
        # label1.place(x= c.SIZE//2, y=c.SIZE//2)

        # canvas = tk.Canvas(self, bg="black", width=30, height=30)
        # canvas.pack()

        # background = tk.PhotoImage(file="background.png")
        # canvas.create_image(350, 200, image=background)

        # character = tk.PhotoImage(file="block2.gif")
        # canvas.create_image(30, 30, image=character)

        self.grid_cells = []
        self.init_grid()
        self.matrix = logic.new_game(c.GRID_LEN)
        self.history_matrixs = []
        self.update_grid_cells()



        # img = tk.Label(self, image=self.blockImg, bg="white")
        # img.place(x=100, y=100)
        # self.grid_cells[1][0].wm_attributes('-transparentcolor', 'white')



        # panel = tk.Label(self.grid_cells[i+1][j], image=self.blockImg2)
        # panel.pack(side="bottom", fill="both", expand="yes")

        # block image
        # im = Image.open(path)
        # im.show()

        self._t_effector2 = threading.Thread(target=self.timer)
        self._t_effector2.daemon = True
        self._t_effector2.start()

        self._t_effector3 = threading.Thread(target=self.frozen)
        self._t_effector3.daemon = True
        self._t_effector3.start()

        self.mainloop()

    def init_grid(self):
        background = Frame(self, bg=c.BACKGROUND_COLOR_GAME,width=c.SIZE, height=c.SIZE+1)
        background.grid()
        # background(self, image=self.blockImg)

        # background.paste(self.blockImg, (c.SIZE//2, c.SIZE//2), self.blockImg)

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
            columnspan=c.GRID_LEN,
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
            width=int(5*c.GRID_LEN+0.5*(c.GRID_LEN)),
            height=2)
        t.grid()
        grid_row.append(t)

        self.grid_cells.append(grid_row)

        for i in range(1,c.GRID_LEN+1):
            grid_row = []
            for j in range(c.GRID_LEN):
                cell = Frame(
                    background,
                    bg=c.BACKGROUND_COLOR_GAME,
                    width=c.SIZE / c.GRID_LEN,
                    height=c.SIZE / c.GRID_LEN
                )
                cell.grid(
                    row=i,
                    column=j,
                    padx=c.GRID_PADDING,
                    pady=c.GRID_PADDING
                )
                t = tk.Canvas(
                    master=cell,
                    # text="",
                    bg=c.BACKGROUND_COLOR_CELL_EMPTY,
                    # justify=CENTER,
                    # font=c.FONT,
                    width=150,
                    height=150,
                    # image=self.blockImg
                )
                text_id = t.create_text(
                    75,
                    75,
                    justify=CENTER,
                    font=c.FONT,
                    text="")
                image_container = t.create_image(100,100, image=self.blockImg)
                t.text = text_id
                t.image = image_container
                t.grid()
                grid_row.append(t)
            self.grid_cells.append(grid_row)

        self.background = background

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

    def update_grid_frost(self, image):
        for i in range(0,c.GRID_LEN):
            for j in range(c.GRID_LEN):
                self.grid_cells[i+1][j].itemconfig(
                    self.grid_cells[i+1][j].image,
                    image=image
                )


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
                    self.grid_cells[i+1][j].configure(bg=c.BACKGROUND_COLOR_CELL_EMPTY)
                    self.grid_cells[i+1][j].itemconfig(
                        self.grid_cells[i+1][j].text,
                        text=str("")
                    )
                else:
                    ## origin label object
                    # self.grid_cells[i+1][j].configure(
                    #     text=str(new_number),
                    #     bg=c.BACKGROUND_COLOR_DICT[new_number],
                    #     fg=c.CELL_COLOR_DICT[new_number],
                    #     # image=self.blockImg
                    # )
                    self.grid_cells[i+1][j].itemconfig(
                        self.grid_cells[i+1][j].text,
                        text=str(new_number),
                        fill=c.CELL_COLOR_DICT[new_number]
                    )
                    self.grid_cells[i+1][j].config(
                        bg=c.BACKGROUND_COLOR_DICT[new_number],
                        # fg=c.CELL_COLOR_DICT[new_number],
                    )

                    score += new_number
                    if (new_number > max_num):
                        max_num = new_number
                        max_color_b = c.BACKGROUND_COLOR_DICT[new_number]
                        max_color_f = c.CELL_COLOR_DICT[new_number]
                #
                # panel = tk.Label(self.grid_cells[i+1][j], image=self.blockImg)
                # panel.pack(side="bottom", fill="both", expand="yes")

                ## another method:
                # canvas = tk.Canvas(self.grid_cells[i+1][j])
                # # canvas.pack()
                # canvas.create_image(10, 10, image=self.blockImg)
                # canvas.pack(side="bottom", fill="both", expand="yes")
        self.grid_cells[0][0].configure(
            text="Score: "+str(score),
            bg=max_color_b,
            fg=max_color_f
        )
        self.update_idletasks()

    def key_down(self, event):
        self.lastInput = time.time()
        key = event.keysym
        if key == c.VK_SPACE:
            if self.frozen_flag == False and time.time() - self.lastInput > 3:
                print("Starting Frozen")
            print("No action")
            return
        self.lastTime = time.time()
        print(event)
        print(self.frozen_flag)
        if key == c.KEY_QUIT: exit()
        elif key == c.KEY_CHANGE:
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
            self.background.destroy()
            self.grid_cells = []

            self.init_grid()
            self.update_grid_cells()
            print(len(self.matrix), c.GRID_LEN)
            panel = tk.Label(self.background, image=self.blockImg)
            panel.pack(side="bottom", fill="both", expand="yes")

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

    def timer(self):
        while True:
            if time.time() - self.lastInput > 3:
                print("frozen")
                self.frozen_flag = True

            time.sleep(0.08)
    def frozen(self):
        while True:
            i = 0
            while self.frozen_flag and i < 10:
                self.raw_image.putalpha(int(i*255/10))  # Half alpha; alpha argument must be an int
                # image = self.raw_image.resize((c.SIZE, c.SIZE), Image.ANTIALIAS)
                self.blockImg = ImageTk.PhotoImage(self.raw_image)
                self.update_grid_frost(self.blockImg)
                i += 1
                if i == 6:
                    i = 9
                time.sleep(0.7)
            time.sleep(0.1)


    # def generate_next(self):
    #     index = (gen(), gen())
    #     while self.matrix[index[0]][index[1]] != 0:
    #         index = (gen(), gen())
    #     self.matrix[index[0]][index[1]] = 2
if __name__ == '__main__':
    game_grid = GameGrid()