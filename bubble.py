import random


class Bubble:
    def __init__(self):
        self.board = self.create_board()
        self.zeros = 81
        self.set_bubbles(5)

    @staticmethod
    def create_board():

        board = [[1]*11]

        for _ in range(9):
            board.append([0]*11)
        board.append([1]*11)

        for i in range(1, 10):
            board[i][0] = 1
            board[i][-1] = 1

        return board

    def show_board(self):
        for i in self.board:
            print(i)

    def set_bubbles(self, n):
        m = 0

        while m < n:

            if self.zeros <= n:

                for i, j in enumerate(self.board):
                    for k, l in enumerate(j):
                        if l == 0:
                            self.zeros -= 1
                            self.board[i][k] = random.choice(range(2, 8))
                            q = self.check_lines(i, k)
                            self.delete_bubbles(q)
                            m += 1
            else:
                coord = random.randint(1, 9), random.randint(1, 9)
                if self.board[coord[0]][coord[1]] == 0:
                    self.zeros -= 1
                    self.board[coord[0]][coord[1]] = random.choice(range(2, 8))
                    q = self.check_lines(*coord)
                    self.delete_bubbles(q)
                    m += 1

    def choose_bubble(self, cache_list, x0, y0, x1, y1):

        cache_list.append((x0, y0))

        if x0 == x1 and y0 == y1:
            return True

        else:

            if (x0 + 1, y0) not in cache_list and self.board[x0 + 1][y0] == 0:
                a1 = self.choose_bubble(cache_list, x0 + 1, y0, x1, y1)
            else:
                a1 = False

            if (x0 - 1, y0) not in cache_list and self.board[x0 - 1][y0] == 0:
                a2 = self.choose_bubble(cache_list, x0 - 1, y0, x1, y1)
            else:
                a2 = False

            if (x0, y0 + 1) not in cache_list and self.board[x0][y0 + 1] == 0:
                a3 = self.choose_bubble(cache_list, x0, y0 + 1, x1, y1)
            else:
                a3 = False

            if (x0, y0 - 1) not in cache_list and self.board[x0][y0 - 1] == 0:
                a4 = self.choose_bubble(cache_list, x0, y0 - 1, x1, y1)
            else:
                a4 = False

            return a1 or a2 or a3 or a4

    def check_lines(self, x, y):

        n = self.board[x][y]

        lst1 = [(x, y)]  # horizontal line
        lst2 = [(x, y)]  # Vertical line
        lst3 = [(x, y)]  # Diagonal line 1
        lst4 = [(x, y)]  # Diagonal line 2

        d = {(1, 0): lst1, (0, 1): lst2, (1, -1): lst3, (1, 1): lst4}

        for c, lst in d.items():

            for i in range(1, 5):
                if self.board[x + c[0] * i][y + c[1] * i] == 1:
                    break
                elif self.board[x + c[0]*i][y+ c[1]*i] == n:
                    lst.append((x + c[0] * i, y + c[1] * i))
                else:
                    break
            for i in range(1, 5):
                if self.board[x - c[0] * i][y - c[1] * i] == 1:
                    break
                elif self.board[x - c[0] * i][y - c[1] * i] == n:
                    lst.append((x - c[0] * i, y - c[1] * i))
                else:
                    break

        return lst1, lst2, lst3, lst4

    def game(self):

        if self.zeros == 0:
            print('Game Over')

        self.show_board()
        while True:

            a, b = input('Select bubble: ').split()
            a, b = int(a), int(b)

            if self.board[a][b] == 0:
                print('You have selected square without bubble. Try again.')
                continue
            else:
                h = self.board[a][b]
                c, d = input('Select target: ').split()
                c, d = int(c), int(d)

            p = self.choose_bubble([], a, b, c, d)

            if not p:
                print('Not allowed move')
                continue

            else:
                self.board[a][b] = 0
                self.board[c][d] = h

            q = self.check_lines(c, d)
            f = self.delete_bubbles(q)
            if f:
                self.set_bubbles(3)
            self.show_board()

    def delete_bubbles(self, d):
        f = True
        for i in d:
            if len(i) > 4:
                self.zeros += len(i)
                f = False
                for j in i:
                    self.board[j[0]][j[1]] = 0

        return f

    def new_game(self):
        self.board = self.create_board()
        self.zeros = 81
        self.set_bubbles(5)


if __name__ == "__main__":

    bubble = Bubble()
    bubble.game()
