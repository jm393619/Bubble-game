import tkinter as tk
import bubble as blb
from tkinter import messagebox


class Bubble(tk.Tk):
    def __init__(self):
        super().__init__()

        self.geometry("600x570+300+100")
        self.title('Bubble')
        self.config(bg='#a9dec1')

        # Create frame with board
        self.frame = tk.Frame(self, bg='black', borderwidth=2, relief='solid')
        self.frame.pack(pady=20)

        # Create Squares on board where there will be bubbles
        self.field_labels = {}
        for i in range(1, 10):
            for j in range(1, 10):
                self.field_labels[tk.Label(self.frame, bg='#a9dec1', font=(None, 25), borderwidth=2,  relief='solid')] \
                    = f'{i}-{j}'

        for i, j in self.field_labels.items():
            q = j.split('-')
            i.grid(row=int(q[0]), column=int(q[1]))

        self.fields_position = {x: y for y, x in self.field_labels.items()}

        self.red = tk.PhotoImage(file=r"colors\red.png")
        self.green = tk.PhotoImage(file=r"colors\green.png")
        self.blue = tk.PhotoImage(file=r"colors\blue.png")
        self.grey = tk.PhotoImage(file=r"colors\grey.png")
        self.yellow = tk.PhotoImage(file=r"colors\yellow.png")
        self.pink = tk.PhotoImage(file=r"colors\pink.png")
        self.white = tk.PhotoImage(file=r"colors\white.png")

        self.colors = {0: self.white, 2: self.red, 3: self.green, 4: self.blue, 5: self.grey, 6: self.yellow,
                       7: self.pink}

        self.bubble = blb.Bubble()

        self.update_board()

        self.bind("<Button-1>", self.game)

        self.clicked_square = None
        self.target_square = None
        # a, b - coordinates of clicked square, c, d - coordinates of target square.
        self.a, self.b, self.c, self.d = -1, -1, -1, -1

        self.menu = tk.Menu(self)
        self.config(menu=self.menu)
        self.menu.add_command(label='New game', command=self.new_game)

    def update_board(self):
        for i, j in self.field_labels.items():
            q1, q2 = (int(x) for x in j.split('-'))

            i.config(image=self.colors[self.bubble.board[q1][q2]])

    def new_game(self):
        self.bubble.new_game()
        self.update_board()

    def game(self, e):
        try:

            q1, q2 = (int(x) for x in self.field_labels[e.widget].split('-'))

            if self.bubble.board[q1][q2] != 0:
                self.clicked_square = e.widget
                self.a, self.b = q1, q2

            elif e.widget == self.clicked_square:
                self.clicked_square = None

            elif self.bubble.board[q1][q2] == 0 and self.clicked_square and not self.target_square:
                self.target_square = e.widget
                self.c, self.d = q1, q2

            elif e.widget == self.target_square:
                self.target_square = None

            # game
            if self.a > 0 and self.b > 0 and self.c > 0 and self.d > 0:
                p = self.bubble.choose_bubble([], self.a, self.b, self.c, self.d)
                if p:
                    self.bubble.board[self.a][self.b], self.bubble.board[self.c][self.d] \
                        = self.bubble.board[self.c][self.d], self.bubble.board[self.a][self.b]

                    self.target_square = None
                    self.clicked_square = None

                    p2 = self.bubble.check_lines(self.c, self.d)

                    p3 = self.bubble.delete_bubbles(p2)

                    self.a, self.b, self.c, self.d = -1, -1, -1, -1

                    if p3:

                        self.bubble.set_bubbles(3)

                    self.update_board()

                else:
                    self.target_square = None
                    self.clicked_square = None
                    self.a, self.b, self.c, self.d = -1, -1, -1, -1

            if self.bubble.zeros <= 0:
                messagebox.showinfo(title='Game Over', message='You have lost')
        except KeyError:
            pass


if __name__ == "__main__":
    bubble = Bubble()
    bubble.mainloop()
