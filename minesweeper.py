import itertools
import random

class Minesweeper():
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines


class Sentence():
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """
        if len(self.cells) == self.count:
            return self.cells
        else:
            return set()

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        if self.count == 0:
            return self.cells
        else:
            return set()

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        if cell in self.cells:
            self.cells.remove(cell)
            self.count -= 1
        return None

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        if cell in self.cells:
            self.cells.remove(cell)
        return None


class MinesweeperAI():
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = []

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)

    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.

        This function should:
            1) mark the cell as a move that has been made
            2) mark the cell as safe
            3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
        """
        # Step 1: Mark the cell as a move made
        self.moves_made.add(cell)

        # Step 2: Mark the cell as safe        
        if cell not in self.safes:
            self.mark_safe(cell)
        
        # Step 3: Determine neighboring cells
        neighbours = set()
        for i in range(cell[0]-1,cell[0]+2):
            for j in range(cell[1]-1, cell[1]+2):
                if 0<=i and i < self.height and 0 <= j and j < self.width:
                    neighbours.add((i,j))
        if cell in neighbours:
            neighbours.remove(cell)

        # Step 4: Filter out known mines, safes, and moves made
        removal = set()
        for n in neighbours.copy():
            if n in self.mines:    
                removal.add(n)
                count -= 1
            if n in self.safes or n in self.moves_made:     
                removal.add(n)
        neighbours -= removal
        
        # Step 5: Add a new sentence to the knowledge base
        sentence = Sentence(neighbours,count)
        if sentence not in self.knowledge:
            self.knowledge.append(sentence)    

        # Step 6: Mark additional cells as safe or mines based on knowledge
        safe_cells = set()
        mine_cells = set()
        for s in self.knowledge.copy():
            km = s.known_mines()
            ks = s.known_safes()
            mine_cells.update(km)  
            safe_cells.update(ks)
            
        for mine in mine_cells:
            self.mark_mine(mine)
        for safe in safe_cells:
            self.mark_safe(safe)

        # Step 7: Infer new sentences from existing knowledge
        new = []
        for s1 in self.knowledge:
            for s2 in self.knowledge:
                if s1 == s2 or len(s1.cells)==0 or len(s2.cells)==0:
                    continue
                elif s1.cells.issubset(s2.cells):
                    new_s = Sentence(s2.cells-s1.cells, s2.count-s1.count)
                    if new_s not in self.knowledge and new_s not in new:
                        new.append(new_s)
        self.knowledge.extend(new)

    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        for i in range(self.height):
            for j in range(self.width):
                if (i,j) not in self.moves_made and (i,j) in self.safes:
                    return (i,j)
        return None

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        options = []
        for i in range(self.height):
            for j in range(self.width):
                if (i,j) not in self.moves_made:
                    if (i,j) not in self.mines:
                        options.append((i,j))
        if options:     
            return random.choice(options)
        else:   
            return None
