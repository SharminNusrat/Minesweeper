import random

class Minesweeper():
    def __init__(self, height=8, width=8, mines=10):
        self.height = height
        self.width = width
        self.mines = set()
        self.board = []

        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)
        
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True
        
        self.mines_found = set()
    
    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]
    
    def nearby_mines(self, cell):
        count = 0

        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):
                if (i, j) == cell:
                    continue

                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1
        
        return count
    
    def won(self):
        return self.mines_found == self.mines