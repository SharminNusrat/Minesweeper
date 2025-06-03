import random

class Sentence:
    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count
    
    def known_mines(self):
        return self.cells if self.count == len(self.cells) else set()
    
    def known_safes(self):
        return self.cells if self.count == 0 else set()
    
    def mark_mine(self, cell):
        if cell in self.cells:
            self.cells.remove(cell)
            self.count -= 1

    def mark_safe(self, cell):
        if cell in self.cells:
            self.cells.remove(cell)
        
class MinesweeperAI:
 
    def __init__(self, height=8, width=8):
        self.height = height
        self.width = width
        self.moves_made = set()
        self.mines = set()
        self.safes = set()
        self.knowledge = []

    def mark_mine(self, cell):
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)

    def add_knowledge(self, cell, count):
        self.moves_made.add(cell)
        self.mark_safe(cell)
        
        neighbors = set()
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):
                if (i, j) == cell:
                    continue
                if 0 <= i < self.height and 0 <= j < self.width:
                    if (i, j) in self.mines:
                        count -= 1
                    elif (i, j) not in self.safes and (i, j) not in self.moves_made:
                        neighbors.add((i, j))
        
        new_sentence = Sentence(neighbors, count)
        self.knowledge.append(new_sentence)
        
        # Inference and cleanup 
        self._update_knowledge()

    def _update_knowledge(self):
        changed = True
        while changed:
            changed = False
            
            for sentence in self.knowledge[:]:
                for safe in sentence.known_safes().copy():
                    if safe not in self.safes:
                        self.mark_safe(safe)
                        changed = True
                for mine in sentence.known_mines().copy():
                    if mine not in self.mines:
                        self.mark_mine(mine)
                        changed = True
            
            self.knowledge = [s for s in self.knowledge if len(s.cells) > 0]
            
            # Infer new knowledge
            new_sentences = []
            for s1 in self.knowledge:
                for s2 in self.knowledge:
                    if s1 != s2 and s1.cells.issubset(s2.cells):
                        new_cells = s2.cells - s1.cells
                        new_count = s2.count - s1.count
                        new_s = Sentence(new_cells, new_count)
                        if new_s not in self.knowledge and new_s not in new_sentences:
                            new_sentences.append(new_s)
                            changed = True
            self.knowledge += new_sentences

    def make_safe_move(self):
        for cell in self.safes:
            if cell not in self.moves_made:
                return cell
        return None

    def make_random_move(self):
        possible_moves = []
        for i in range(self.height):
            for j in range(self.width):
                if (i, j) not in self.moves_made and (i, j) not in self.mines:
                    possible_moves.append((i, j))
        return random.choice(possible_moves) if possible_moves else None