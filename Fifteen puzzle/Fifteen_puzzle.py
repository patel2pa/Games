import poc_fifteen_gui

#import codeskulptor
#codeskulptor.set_timeout(60)

class Puzzle:
    """
    Class representation for the Fifteen puzzle
    """

    def __init__(self, puzzle_height, puzzle_width, initial_grid=None):
        """
        Initialize puzzle with default height and width
        Returns a Puzzle object
        """
        self._height = puzzle_height
        self._width = puzzle_width
        self._grid = [[col + puzzle_width * row
                       for col in range(self._width)]
                      for row in range(self._height)]

        if initial_grid != None:
            for row in range(puzzle_height):
                for col in range(puzzle_width):
                    self._grid[row][col] = initial_grid[row][col]

    def __str__(self):
        """
        Generate string representaion for puzzle
        Returns a string
        """
        ans = ""
        for row in range(self._height):
            ans += str(self._grid[row])
            ans += "\n"
        return ans

    #####################################
    # GUI methods

    def get_height(self):
        """
        Getter for puzzle height
        Returns an integer
        """
        return self._height

    def get_width(self):
        """
        Getter for puzzle width
        Returns an integer
        """
        return self._width

    def get_number(self, row, col):
        """
        Getter for the number at tile position pos
        Returns an integer
        """
        return self._grid[row][col]

    def set_number(self, row, col, value):
        """
        Setter for the number at tile position pos
        """
        self._grid[row][col] = value

    def clone(self):
        """
        Make a copy of the puzzle to update during solving
        Returns a Puzzle object
        """
        new_puzzle = Puzzle(self._height, self._width, self._grid)
        return new_puzzle

    ########################################################
    # Core puzzle methods

    def current_position(self, solved_row, solved_col):
        """
        Locate the current position of the tile that will be at
        position (solved_row, solved_col) when the puzzle is solved
        Returns a tuple of two integers        
        """
        solved_value = (solved_col + self._width * solved_row)

        for row in range(self._height):
            for col in range(self._width):
                if self._grid[row][col] == solved_value:
                    return (row, col)
        assert False, "Value " + str(solved_value) + " not found"

    def update_puzzle(self, move_string):
        """
        Updates the puzzle state based on the provided move string
        """
        zero_row, zero_col = self.current_position(0, 0)
        for direction in move_string:
            if direction == "l":
                assert zero_col > 0, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row][zero_col - 1]
                self._grid[zero_row][zero_col - 1] = 0
                zero_col -= 1
            elif direction == "r":
                assert zero_col < self._width - 1, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row][zero_col + 1]
                self._grid[zero_row][zero_col + 1] = 0
                zero_col += 1
            elif direction == "u":
                assert zero_row > 0, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row - 1][zero_col]
                self._grid[zero_row - 1][zero_col] = 0
                zero_row -= 1
            elif direction == "d":
                assert zero_row < self._height - 1, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row + 1][zero_col]
                self._grid[zero_row + 1][zero_col] = 0
                zero_row += 1
            else:
                assert False, "invalid direction: " + direction

    ##################################################################
    # Phase one methods

    ##################################################################
    # lower_row_invariant methods
    def lower_row_invariant(self, target_row, target_col):
        """
        Check whether the puzzle satisfies the specified invariant
        at the given position in the bottom rows of the puzzle (target_row > 1)
        Returns a boolean
        """
        # replace with your code
        
        #assert self.get_number(target_row, target_col) == 0, \
        #                       "Tile zero is not positioned [target_row][target_col]"
        if self.get_number(target_row, target_col) != 0:
            return False
        if (target_row == (self.get_height() - 1)) and (target_col == (self.get_width() - 1)):
            return True
        
        label = True
        dummy_row = self.get_height() - 1
        dummy_col = self.get_width() - 1
        value = self.get_height() * self.get_width() - 1
        
        while label:           
            #assert self.get_number(dummy_row, dummy_col) == value \
            #                      "Tile not positioned at their solved location"
            if self.get_number(dummy_row, dummy_col) != value:
                return False
            dummy_col -= 1
            if dummy_col < 0:
                dummy_col = self.get_width() - 1
                dummy_row -= 1
            if (dummy_row == target_row) and (dummy_col == target_col):
                label = False
            value -= 1
        return True
    
    ########################################################
    # solve_interior_tile methods

    def solve_interior_tile(self, target_row, target_col):
        """
        Place correct tile at target position
        Updates puzzle and returns a move string
        """
        # replace with your code
        #print self.__str__()
        moving_str = ''
        
        #assert self.lower_row_invariant(target_row, target_col), \
        #       "lower_row_invariant(target_row, target_col+1) not satisfied"
        #assert target_col != 0, "target_col == 0"
        #assert target_row > 1, "target_row <= 1"
                
        target_tmppos = self.current_position(target_row, target_col) 
        
        # target value in the same line as zero tile
        if target_tmppos[0] == target_row:            
            while target_tmppos[1] - target_col != 0:           
                self.update_puzzle('l' * (target_col - target_tmppos[1]))      
                moving_str += 'l' * (target_col - target_tmppos[1])
                target_tmppos = self.current_position(target_row, target_col)          
                if self.lower_row_invariant(target_row, target_col-1):
                    return moving_str             
                self.update_puzzle('ur' + 'r' * (target_col - target_tmppos[1]) + 'd')      
                moving_str += ('ur' + 'r' * (target_col - target_tmppos[1]) + 'd')
                target_tmppos = self.current_position(target_row, target_col)  
          
        # target value above zero tile
        if (target_tmppos[1] == target_col) and (target_row - target_tmppos[0] != 1):
            #if target_row - target_tmppos[0] == 1:
            #    self.update_puzzle('uld')      
            #    moving_str += 'uld'
            #    target_tmppos = self.current_position(target_row, target_col)
            #    return moving_str
            
            self.update_puzzle('u' * (target_row - target_tmppos[0] - 1))      
            moving_str += 'u' * (target_row - target_tmppos[0] - 1)
            target_tmppos = self.current_position(target_row, target_col)  
            #print self.__str__()
            
            
        # target value above and on right side of zero tile
        if target_tmppos[1] > target_col:
            self.update_puzzle('u' * (target_row - target_tmppos[0]))      
            moving_str += 'u' * (target_row - target_tmppos[0])
            target_tmppos = self.current_position(target_row, target_col)                         
            while target_tmppos[1] - target_col != 0:      
                self.update_puzzle('r' * (target_tmppos[1] - target_col) + 'dl')    
                moving_str += ('r' * (target_tmppos[1] - target_col) + 'dl')
                target_tmppos = self.current_position(target_row, target_col)                  
                if target_tmppos[1] - target_col != 0:
                    self.update_puzzle('l' * (target_tmppos[1] - target_col) + 'u')    
                    moving_str += ('l' * (target_tmppos[1] - target_col) + 'u')
                    target_tmppos = self.current_position(target_row, target_col)  

        # target value above and on left side of zero tile
        if target_tmppos[1] < target_col:
            self.update_puzzle('u' * (target_row - target_tmppos[0]))      
            moving_str += 'u' * (target_row - target_tmppos[0])
            target_tmppos = self.current_position(target_row, target_col)  
            #print self.__str__()
            
            while target_col - target_tmppos[1] != 0:        
                self.update_puzzle('l' * (target_col - target_tmppos[1]) + 'dr')    
                moving_str += ('l' * (target_col - target_tmppos[1]) + 'dr')
                target_tmppos = self.current_position(target_row, target_col)  
                #print self.__str__()
                
                if target_col - target_tmppos[1] != 0:
                    self.update_puzzle('r' * (target_col - target_tmppos[1]) + 'u')    
                    moving_str += ('r' * (target_col - target_tmppos[1]) + 'u')
                    target_tmppos = self.current_position(target_row, target_col) 
                    #print self.__str__()
                   
        # preprocess                       
        self.update_puzzle('u') 
        moving_str += ('u')
        target_tmppos = self.current_position(target_row, target_col)        
        #print self.__str__()
        
        if (target_row == target_tmppos[0]) and (target_col == target_tmppos[1]):
            self.update_puzzle('ld') 
            moving_str += ('ld')
            #target_tmppos = self.current_position(target_row, target_col)  
            return moving_str
        
        # cyclic       
        while target_row - self.current_position(target_row, target_col)[0] > 1:
            self.update_puzzle('lddru')
            moving_str += 'lddru'
            #target_tmppos = self.current_position(target_row, target_col) 
            #print self.__str__()
            
           
        self.update_puzzle('lddruld')
        moving_str += 'lddruld'
        #target_tmppos = self.current_position(target_row, target_col)          
        #if self.lower_row_invariant(target_row, target_col-1):
        #print self.__str__()
        return moving_str

    ########################################################
    # solve_col0_tile methods
    
    def solve_col0_tile(self, target_row):
        """
        Solve tile in column zero on specified row (> 1)
        Updates puzzle and returns a move string
        """
        # replace with your code
        #print self.__str__()
        moving_str = ''
        target_tmppos = self.current_position(target_row, 0) 
        
        # target tile right above zero tile
        if (target_tmppos[0] == target_row - 1) and (target_tmppos[1] == 0):
            self.update_puzzle('ur' + 'r' * (self.get_width() - 2))
            moving_str += ('ur' + 'r' * (self.get_width() - 2))
            return moving_str
        
        # target tile above zero tile
        elif (target_tmppos[0] != target_row - 1) and (target_tmppos[1] == 0):
            self.update_puzzle('u' * (target_row - target_tmppos[0]) + 'rdl')      
            moving_str += ('u' * (target_row - target_tmppos[0]) + 'rdl')
            #target_tmppos = self.current_position(target_row, 0)              
            if target_row - self.current_position(target_row, 0)[0] != 1:
                self.update_puzzle('ur')    
                moving_str += ('ur')
                #target_tmppos = self.current_position(target_row, 0)     
                
                # cyclic       
                while target_row - self.current_position(target_row, 0)[0] > 1:
                    self.update_puzzle('lddru')
                    moving_str += 'lddru'
                    target_tmppos = self.current_position(target_row, 0) 
                self.update_puzzle('ld')
                moving_str += 'ld'        

        # target tile above and on the right side of zero tile
        elif (target_tmppos[0] != target_row - 1) and (target_tmppos[1] != 0):
            self.update_puzzle('u' * (target_row - target_tmppos[0]))      
            moving_str += 'u' * (target_row - target_tmppos[0])
            #target_tmppos = self.current_position(target_row, 0)            
            #print self.__str__()
                    
            if target_row - self.current_position(target_row, 0)[0] == 1:
                while target_tmppos[1] != 1:      
                    self.update_puzzle('r' * target_tmppos[1] + 'ul')    
                    moving_str += ('r' * target_tmppos[1] + 'ul')
                    target_tmppos = self.current_position(target_row, 0)     
                    if target_tmppos[1] != 1:
                        self.update_puzzle('l' * target_tmppos[1] + 'd')    
                        moving_str += ('l' * target_tmppos[1] + 'd')
                        target_tmppos = self.current_position(target_row, 0)  
                self.update_puzzle('d')    
                moving_str += ('d')
                target_tmppos = self.current_position(target_row, 0) 
            
            elif target_row - target_tmppos[0] > 1: 
                
                if target_tmppos[1] == 1:
                    self.update_puzzle('dr')    
                    moving_str += ('dr')
                    #target_tmppos = self.current_position(target_row, 0)
                    
                while target_tmppos[1] != 1:      
                    self.update_puzzle('r' * target_tmppos[1] + 'dl')    
                    moving_str += ('r' * target_tmppos[1] + 'dl')
                    target_tmppos = self.current_position(target_row, 0)     
                    
                    if target_tmppos[1] != 1:
                        self.update_puzzle('l' * target_tmppos[1] + 'u')    
                        moving_str += ('l' * target_tmppos[1] + 'u')
                        target_tmppos = self.current_position(target_row, 0)  
                  
                self.update_puzzle('u')    
                moving_str += ('u')
                #target_tmppos = self.current_position(target_row, 0)  
                
                # cyclic       
                while target_row - self.current_position(target_row, 0)[0] > 1:
                    self.update_puzzle('lddru')
                    moving_str += 'lddru'
                    #target_tmppos = self.current_position(target_row, 0) 
                self.update_puzzle('ld')
                moving_str += 'ld'
                
        self.update_puzzle('ruldrdlurdluurddlur' + 'r' * (self.get_width() - 2))    
        moving_str += ('ruldrdlurdluurddlur' + 'r' * (self.get_width() - 2))        
        #print self.__str__()
        return moving_str   

    #############################################################
    # Phase two methods

    ########################################################
    # row0_invariant methods
    
    def row0_invariant(self, target_col):
        """
        Check whether the puzzle satisfies the row zero invariant
        at the given column (col > 1)
        Returns a boolean
        """
        # replace with your code
        
        # check the zero tile
        if self.get_number(0, target_col) != 0:
            return False
        
        # check the tiles after but not include (1, target_col - 1)
        label = True
        dummy_row = self.get_height() - 1
        dummy_col = self.get_width() - 1
        exp_value = self.get_height() * self.get_width() - 1
        
        while label:  
            #print (dummy_row, dummy_col), exp_value
            if self.get_number(dummy_row, dummy_col) != exp_value:
                return False
            dummy_col -= 1
            if (dummy_row == 0) and (dummy_col < 0):
                return True            
            if dummy_col < 0:
                dummy_col = self.get_width() - 1
                dummy_row -= 1
            if (dummy_row == 1) and (dummy_col == target_col - 1):
                label = False
            exp_value -= 1

        
        # check the tiles (from right to left) in row 0 after/include column (target_col + 1)
        exp_value -= target_col
        label = True 
        dummy_col = self.get_width() - 1
        while label:
            if self.get_number(0, dummy_col) != exp_value:
                return False
            exp_value -= 1
            dummy_col -= 1
            if dummy_col == target_col:
                label = False
        return True

    ########################################################
    # row1_invariant methods
    
    def row1_invariant(self, target_col):
        """
        Check whether the puzzle satisfies the row one invariant
        at the given column (col > 1)
        Returns a boolean
        """
        # replace with your code
        if not self.lower_row_invariant(1, target_col):
            return False
        if target_col == self.get_width() - 1:
            return True
        exp_value = self.get_number(1, target_col + 1) - self.get_width()   
        for dummy_col in range(target_col + 1, self.get_width()):
            if exp_value != self.get_number(0, dummy_col):
                return False
            exp_value += 1
        return True

    ########################################################
    # solve_row1_tile methods
    
    def solve_row1_tile(self, target_col):
        """
        Solve the tile in row one at the specified column
        Updates puzzle and returns a move string
        """
        # replace with your code
        moving_str = ''
       
        assert self.row1_invariant(target_col), \
               "row1_invariant(target_col+1) not satisfied"
        
        target1_tmppos = self.current_position(1, target_col)         
        #print 'target1 org', target1_tmppos   
        
        # target1 in row 0 and right above zero tile
        if (target1_tmppos[0] == 0) and (target1_tmppos[1] == target_col):
            self.update_puzzle('uld')      
            moving_str += 'uld'
            target1_tmppos = self.current_position(1, target_col)            
        
        # target1 in row 0 (the above row) as zero tile        
        elif target1_tmppos[0] == 0:
            self.update_puzzle('l' * (target_col - target1_tmppos[1]) + 'u' + 'r' * (target_col - target1_tmppos[1]) + 'd')      
            moving_str += ('l' * (target_col - target1_tmppos[1]) + 'u' + 'r' * (target_col - target1_tmppos[1]) + 'd')
            target1_tmppos = self.current_position(1, target_col)
         
        # now target1 in row 1 (the same row) as zero tile        
         
        while target1_tmppos[1] - target_col != 0:
            self.update_puzzle('l' * (target_col - target1_tmppos[1]))      
            moving_str += 'l' * (target_col - target1_tmppos[1])
            target1_tmppos = self.current_position(1, target_col) 
            if target1_tmppos[1] - target_col == 0:
                break
            self.update_puzzle('ur' + 'r' * (target_col - target1_tmppos[1]) + 'd')      
            moving_str += ('ur' + 'r' * (target_col - target1_tmppos[1]) + 'd')
            target1_tmppos = self.current_position(1, target_col) 
            
        #print 'target1 correct', target1_tmppos    
        # now target1 is put in right position
        
        self.update_puzzle('ur')      
        moving_str += 'ur'
        target1_tmppos = self.current_position(1, target_col)
        
        return moving_str
    
    ########################################################
    # solve_row0_tile methods
    
    def solve_row0_tile(self, target_col):
        """
        Solve the tile in row zero at the specified column
        Updates puzzle and returns a move string
        """
        # replace with your code
        moving_str = ''
        #print obj.__str__()
        self.update_puzzle('ld')      
        moving_str += 'ld'
        target2_tmppos = self.current_position(0, target_col)                                
        #print 'target2 org', target2_tmppos
        #print obj.__str__()
        
        # target2 just in its position (on left side of zero tile from the orginal given)
        if self.row1_invariant(target_col - 1):
            return moving_str
        
        # target2 in row 0 and just above zero tile
        if (target2_tmppos[0] == 0) and (target2_tmppos[1] == target_col - 1):
            self.update_puzzle('uld')      
            moving_str += ('uld')  
            target2_tmppos = self.current_position(0, target_col)
            #print obj.__str__()
        # target2 in row 0 (above zero tile)
        elif target2_tmppos[0] == 0:
            self.update_puzzle('l' * ((target_col-1) - target2_tmppos[1]) + 'u' + 'r' * ((target_col-1) - target2_tmppos[1]) + 'd')      
            moving_str += ('l' * ((target_col-1) - target2_tmppos[1]) + 'u' + 'r' * ((target_col-1) - target2_tmppos[1]) + 'd')
            target2_tmppos = self.current_position(0, target_col) 
        
        
        
        
        
        
        
        # now target2 in row 1 (the same row) as zero tile
        while target2_tmppos[1] - (target_col-1) != 0:
            self.update_puzzle('l' * ((target_col-1) - target2_tmppos[1]))      
            moving_str += ('l' * ((target_col-1) - target2_tmppos[1]))
            target2_tmppos = self.current_position(0, target_col) 
                
            if target2_tmppos[1] - (target_col-1) == 0:
                break
            self.update_puzzle('ur' + 'r' * ((target_col-1) - target2_tmppos[1]) + 'd')      
            moving_str += ('ur' + 'r' * ((target_col-1) - target2_tmppos[1]) + 'd')
            target2_tmppos = self.current_position(0, target_col) 
        
        # cyclic
        self.update_puzzle('urdlurrdluldrruld')      
        moving_str += 'urdlurrdluldrruld'
        target2_tmppos = self.current_position(0, target_col)    
        #print obj.__str__()
        #print 'target2 correct', target2_tmppos
        #if self.row0_invariant(target_col - 1):
        return moving_str

    ###########################################################
    # Phase 3 methods

    ###########################################################
    # solve_2x2 methods
    def solve_2x2(self):
        """
        Solve the upper left 2x2 part of the puzzle
        Updates the puzzle and returns a move string
        """
        # replace with your code
        moving_str = ''
        
        while not self.lower_row_invariant(0, 0):
            self.update_puzzle('u')      
            moving_str += 'u'
            if not self.lower_row_invariant(0, 0):
                self.update_puzzle('l')      
                moving_str += 'l'
                if not self.lower_row_invariant(0, 0):
                    self.update_puzzle('d')      
                    moving_str += 'd'
                    if not self.lower_row_invariant(0, 0):
                        self.update_puzzle('r')      
                        moving_str += 'r'  
        return moving_str 
    
    ###########################################################
    # solve_puzzle methods

    def solve_puzzle(self):
        """
        Generate a solution string for a puzzle
        Updates the puzzle and returns a move string
        """
        # replace with your code
        moving_str = ''
        #print self.__str__()
        
        zero_tile_pos = (0, 0)
        for dummy_row in range(self.get_height()):

            for dummy_col in range(self.get_width()):
                #print (dummy_row, dummy_col)
                #print self.get_number(dummy_row, dummy_col)
                if self.get_number(dummy_row, dummy_col) == 0:
                    zero_tile_pos = (dummy_row, dummy_col)
                    #print zero_tile_pos
        #print self.__str__()
        #print zero_tile_pos
        
    
        self.update_puzzle('r' * ((self.get_width() - 1) - zero_tile_pos[1]))      
        moving_str += ('r' * ((self.get_width() - 1) - zero_tile_pos[1]))
        
        self.update_puzzle('d' * ((self.get_height() - 1) - zero_tile_pos[0]))      
        moving_str += ('d' * ((self.get_height() - 1) - zero_tile_pos[0]))
                              
        dummy_row = self.get_height() - 1
        dummy_col = self.get_width() - 1
        
        label = True
        #print self.__str__()
        
        while label:
            
            #print (dummy_row, dummy_col)
            #print self.lower_row_invariant(dummy_row, dummy_col) or self.row1_invariant(dummy_col) or self.row0_invariant(dummy_col)
            #print '********************'
         
            if (dummy_row > 1) and (dummy_col > 0):
                #print 'start solve_interior_tile'
                moving_str += self.solve_interior_tile(dummy_row, dummy_col)
                dummy_col -= 1   
                #print self.__str__()
                #print 'end solve_interior_tile'
                #print
                
            elif (dummy_row > 1) and (dummy_col == 0):
                #print 'start solve_col0_tile'
                moving_str += self.solve_col0_tile(dummy_row)
                dummy_row -= 1
                dummy_col = self.get_width() - 1   
                #print self.__str__()
                #print 'end solve_col0_tile'
                #print
            elif (dummy_row == 1) and (dummy_col > 1):
                #print 'start solve_row1_tile'
                moving_str += self.solve_row1_tile(dummy_col)
                dummy_row = 0
                #print self.__str__()
                #print 'end solve_row1_tile'
                #print
            elif (dummy_row == 0) and (dummy_col > 1):
                #print 'start solve_row0_tile'
                moving_str += self.solve_row0_tile(dummy_col)
                dummy_row = 1
                dummy_col -= 1
                #print self.__str__()
                #print 'end solve_row0_tile'
                #print
            elif (dummy_row < 2) and (dummy_col < 2):
                moving_str += self.solve_2x2()
            
            #print self.__str__()
            
            if self.lower_row_invariant(0, 0):
                print self.__str__()
                return moving_str

#obj = Puzzle(3, 6, [[16, 7, 13, 17, 5, 9], [3, 0, 14, 10, 12, 6], [4, 15, 2, 11, 8, 1]])
#print obj.solve_puzzle() #returned incorrect move string (Exception: AssertionError) "move off grid: d" at line 121, in update_puzzle

#obj = Puzzle(3, 6, [[3, 10, 5, 7, 13, 9], [14, 12, 1, 2, 11, 8], [4, 6, 0, 15, 16, 17]])
#print obj.solve_interior_tile(2, 2) #returned incorrect move string (Exception: AssertionError) "move off grid: d" at line 121, in update_puzzle


#obj = Puzzle(4, 5, [[15, 16, 0, 3, 4], [5, 6, 7, 8, 9], [10, 11, 12, 13, 14], [1, 2, 17, 18, 19]])
#print obj.solve_puzzle() #returned incorrect move string (Exception: AssertionError) "move off grid: d" at line 118, in update_puzzle            

#obj = Puzzle(4, 5, [[5, 6, 0, 3, 4], [1, 2, 7, 8, 9], [10, 11, 12, 13, 14], [15, 16, 17, 18, 19]])
#print obj.__str__()
#print obj.solve_row0_tile(2) #returned incorrect move string (Exception: AssertionError) "move off grid: d" at line 118, in update_puzzle            
#print obj.__str__()

#obj = Puzzle(4, 5, [[5, 6, 3, 4, 9], [1, 2, 7, 8, 0], [10, 11, 12, 13, 14], [15, 16, 17, 18, 19]])
#print obj.__str__()
#print obj.solve_row1_tile(4)
#print obj.__str__()

#obj = Puzzle(4, 5, [[5, 15, 3, 4, 9], [6, 10, 7, 8, 14], [2, 1, 11, 12, 13], [0, 16, 17, 18, 19]])
#print obj.solve_col0_tile(3)

#obj = Puzzle(4, 5, [[15, 16, 3, 4, 9], [5, 6, 7, 8, 14], [10, 2, 11, 12, 13], [1, 0, 17, 18, 19]])
#print obj.solve_interior_tile(3, 1)


#obj = Puzzle(3, 3, [[0, 1, 2], [3, 4, 5], [6, 7, 8]])
#print obj.solve_puzzle() #returned incorrect move string (Exception: AssertionError) "lower_row_invariant(target_row, target_col+1) not satisfied" at line 177, in solve_interior_tile   
    
#obj = Puzzle(3, 3, [[8, 7, 6], [5, 4, 3], [2, 1, 0]])
#print obj.solve_puzzle() #returned incorrect move string ''

    
#Start interactive simulation
#poc_fifteen_gui.FifteenGUI(Puzzle(3, 3))
