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
    
    #list of known mines
    mines = set()
    
    #list of known safe
    safe = set()
    
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
        #return all the cells if all of them is mine
        if self.count == len(self.cells):
            for i in self.cells:
                self.mines.add(i)
            return self.mines
        return None
        
    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        #return all the cells if non of them is mine
        if self.count == 0:
            for i in self.cells:
                self.safe.add(i)
            return self.safe
        return None

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        #iterate over all the cells to know if the cells exist in the sentence or not
        if cell in self.cells: 
            self.count = self.count - 1
            self.cells.remove(cell)
        return None

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        #iterate over all the cells to know if the cells exist in the sentence or not
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
        """
       
        #add the cell to the moves that have been made
        self.moves_made.add(cell)  
        
        #add the cell to the safe cells
        self.mark_safe(cell)
        
        #add a new sentence to the AI's knowledge base
        neighbors = []
        for i in range (cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):
                if (i, j) == cell:
                    continue
        #check that the neighbors is not out of the cell range
                if i > 7 or j > 7 or i < 0 or j <0:
                    continue
                neighbors.append((i,j)) 

        s = Sentence(neighbors, count)
        
        if s not in self.knowledge:
            self.knowledge.append(s)
        else:
            return None
                         
        #check if any of the new sentence cells is a mine
        s_mines = set()        
        for c in s.cells:
            if c in self.mines:
                s_mines.add(c)
        for c in s_mines:
            s.mark_mine(c)
        
            
        #check if any of the new sentence cells is safe
        s_safes = set()        
        for c in s.cells:
            if c in self.safes:
                s_safes.add(c)
        for c in s_safes:
            s.mark_safe(c)
      
        
        
        #check if all of the new sentence cells is mine    
        if len(s.cells) == s.count and len(s.cells)>1:
             new_mines= s.known_mines()  
             for i in new_mines:
                self.mark_mine(i)
        #iterate over sentneces in knowledge to see if there is new inferring
             for x in self.knowledge: 
                 if x.known_safes() != None:
                    for y in x.cells:
                        self.safes.add(y)
  
             
        #check if all of the new sentence cells is safe
        if s.count == 0 and len(s.cells) > 0:
           new_safes= s.known_safes()
           for i in new_safes:
                self.mark_safe(i)
       #iterate over the sentneces in knowledge to see if there is new inferring
           for x in self.knowledge: 
              if x.known_mines() != None:
                  for y in x.cells:
                      self.mines.add(y)
        

        
        #conclude new information by comparing the new sentence with the rest sentneces in our knowledge
        if len(self.knowledge) > 1:
            
            new_knowledge = []
            for sentence in self.knowledge:
               
                if s.cells.issubset(sentence.cells):     
                    common = s.cells.intersection(sentence.cells)
                    new_cells = sentence.cells.difference(common)
                    new_count = sentence.count - s.count
                    new_sentence = Sentence(new_cells, new_count)
                
                
                    if len(new_cells) == new_count:
                        for n in new_cells:
                            self.mark_mine(n)
                
                    if new_count == 0:
                        for n in new_cells:
                            self.mark_safe(n)
                            
                    new_knowledge.append(new_sentence)
                    
        
                if sentence.cells.issubset(s.cells):                
                    common = s.cells.intersection(sentence.cells)
                    new_cells = s.cells.difference(common)
                    new_count = s.count - sentence.count
                    new_sentence = Sentence(new_cells, new_count)
                
                
                    if len(new_cells) == new_count:
                        for n in new_cells:
                            self.mark_mine(n)
                
                    if new_count == 0:
                        for n in new_cells:
                            self.mark_safe(n)
                                                
                    new_knowledge.append(new_sentence)
         
            for i in new_knowledge:
                if i not in self.knowledge:
                    self.knowledge.append(i)
                    
            

    def make_safe_move(self):
        for s_move in self.safes:
            if s_move in self.moves_made:
                continue
            return s_move
        return None
    
    
    def make_random_move(self):
       counter = 0 
       while counter < 100:
            i = random.randrange(self.height)
            j = random.randrange(self.width)
            if (i, j) in self.mines or (i, j) in self.moves_made:
                counter = counter +1
                continue
            return (i, j)
       return None