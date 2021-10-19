from gameboard import *

class MyPlayer:
    """
    Class to create a player to play the game
    """
    
    def __init__(self, w, h, method = "simple"):
        """
        Initialitzation of the player with the dimensions of its board and its level
        Returns nothing
        Arguments:
            w -> width of the board
            h -> height of the board
            method -> level of the player, "simple" if not given
        Preconditions:
            w and h must be positive integers
            method must be either "simple" or "expert" if given
        """
        
        # creation of the board to be played in
        try:
            self._board = GameBoard(Shape(w, h))
        except Exception as ex:
            # the given arguments were not valid
            raise ex
        
        #  initialitzation of boolean _simple, to store the method
        if method == "simple":
            self._simple = True
        elif method == "expert":
            self._simple = False
        else:
            raise Exception("Demanded method doesn't exist")
    
    
    def __str__(self):
        return self._board.__str__()
    
    
    def _clear_full(self):
        """
        Auxiliar method to clear all full rows and columns
        Returns nothing
        """
        
        full_columns = self._board.full_columns()
        full_rows = self._board.full_rows()
        self._board.clear_rows(full_rows)
        self._board.clear_columns(full_columns)
    
    
    def place_block(self, placeLocation, placeShape = Shape(1, 1)):
        """
        Method to place a rectangle
        Returns the player itself
        Arguments:
            placeLocation -> The location of bottom left square of the rectangle
            placeShape -> The shape of the rectangle, optional argument
        Preconditions:
            placeLocation and placeShape are a valid location and shape, respectively
            The rectangle to be placed is empty
        """
        
        # place the block
        try:
            self._board.put(placeLocation, placeShape)
        except Exception as ex:
            # the preconditions were not fulfilled
            raise ex
        
        # clear rows and columns that have been filled
        self._clear_full()
        
        return self
    
    
    def is_legal(self, checkShape):
        """
        Method that returns if a shape is legal
        Arguments:
            checkShape -> Shaped to be checked
        """
        
        if not isinstance(checkShape, Shape):
            return False
        if not isinstance(checkShape.width, int) or not isinstance(checkShape.height, int):
            return False
        if checkShape.width < 1 or checkShape.height < 1:
            return False
        if checkShape.width > self._board.get_shape().width or checkShape.height > self._board.get_shape().height:
            return False
        
        return True
    
    
    def play(self, placeShape):
        """
        Method to play a given shape. Its positioning depends on the level of the player
        Returns the location decided to place the shape
        Arguments:
            placeShape -> shape to be placed
        """
        
        # chcking the shape is legal
        if not self.is_legal(placeShape):
            raise Exception("The shape is not legal")
        

        if self._simple:
            # simple player
            # checks in order where can it place the shape and returns the first possible
            for r in range(self._board.get_shape().height):
                for c in range(self._board.get_shape().width):
                    try:
                        if self._board.is_empty(Location(row=r, column=c), placeShape):
                            return Location(row=r, column=c)
                    except:
                        continue
            return None
        
        else:
            # expert player
            # punctuates all posible placing spots and returns the best
            best_punct = -1000000
            best_Location = None
            
            for r in range(self._board.get_shape().height - placeShape.height +1):
                for c in range(self._board.get_shape().width - placeShape.width +1):
                    
                    # if the location is a posible placing spot
                    if self._board.is_empty(Location(row=r, column=c), placeShape):
                        # punctuate it
                        punct = self._punctuation(Location(row=r, column=c), placeShape)
                        if punct > best_punct:
                            best_punct = punct
                            best_Location = Location(row=r, column=c)
                    
            return best_Location


    def _punctuation(self, checkLocation, checkShape):
        """
        Method that returns the punctuation of a location to place a shape
        It considers different things that add up to the final punctuation
        Arguments:
            checkLocation -> The location to be punctuated
            checkShape -> shape to be placed
        """
        
        # initialitzation of some variables
        # its optimal value has been found experimentally
        x = [101.73623919534931, 102.59966534850058, 10179.484568034057, -965.5994719665939, 0.009403568796147519, 5.690955955544556]
        
        self._suma_adjacent = x[0]
        self._suma_borde = x[1]
        self._petar = x[2]
        self._petar_voltant = x[3] 
        self._casi_petar = x[4]
        self._resta_diag = x[5]
        
        # initially, x was [100, 98, 10000, -1000, 0.01, 6]
        
        
        punctuation = 0
        
        
        # for each adjacent block (not diagonaly):
            # if it belongs to the border: sum some value, "self._suma_borde"
            # else if it is full: sum another value (slighly bigger), "self._suma_adjacent"
        for i in range(checkShape.width):
            if checkLocation.row == 0 or checkLocation.column + i >= self._board.get_shape().width:
                punctuation += self._suma_borde
            elif self._board.is_full(Location(checkLocation.row-1, checkLocation.column + i)):
                punctuation += self._suma_adjacent
                
            if checkLocation.row+checkShape.height >= self._board.get_shape().height or checkLocation.column + i >= self._board.get_shape().width:
                punctuation += self._suma_borde
            elif self._board.is_full(Location(checkLocation.row+checkShape.height, checkLocation.column + i)):
                punctuation += self._suma_adjacent
                
        for i in range(checkShape.height):
            if (checkLocation.column == 0 or checkLocation.row + i >= self._board.get_shape().height):
                punctuation += self._suma_borde
            elif self._board.is_full(Location(checkLocation.row+i, checkLocation.column-1)):
                punctuation += self._suma_adjacent
                
            if checkLocation.column+checkShape.width >= self._board.get_shape().width or checkLocation.row + i >= self._board.get_shape().height:
                punctuation += self._suma_borde
            elif self._board.is_full(Location(checkLocation.row+i, checkLocation.column + checkShape.width)):
                punctuation += self._suma_adjacent
                
        
        if punctuation == 0:
            return 0
        
        
        # for each diagonally adjacent block:
            # if it belongs to the border or is full: subtract a value, "self._resta_diag"
        if checkLocation.row == 0 or checkLocation.column == 0:
            punctuation -= self._resta_diag
        elif self._board.is_full(Location(checkLocation.row-1, checkLocation.column-1)):
            punctuation -= self._resta_diag
           
        if checkLocation.row == 0 or checkLocation.column + checkShape.width == self._board.get_shape().width:
            punctuation -= self._resta_diag
        elif self._board.is_full(Location(checkLocation.row-1, checkLocation.column + checkShape.width)):
            punctuation -= self._resta_diag
        
        if checkLocation.row + checkShape.height == self._board.get_shape().height or checkLocation.column + checkShape.width == self._board.get_shape().width:
            punctuation -= self._resta_diag
        elif self._board.is_full(Location(checkLocation.row + checkShape.height, checkLocation.column + checkShape.width)):
            punctuation -= self._resta_diag
        
        if checkLocation.row + checkShape.height == self._board.get_shape().height or checkLocation.column == 0:
            punctuation -= self._resta_diag
        elif self._board.is_full(Location(checkLocation.row + checkShape.height, checkLocation.column-1)):
            punctuation -= self._resta_diag
            
        
        # for each row and column:
            # if it will be filled:
                # add its counter times a value, "self._petar"
                # and subtract the counter of its nearbies times another value, "self._petar_voltant"
            # else:
                # add its counter times a value, "self._casi_petar"
        column_counters = self._board.column_counters()
        row_counters = self._board.row_counters()
        for i in range(checkShape.height):
            if row_counters[i + checkLocation.row] == self._board.get_shape().width-checkShape.width:
                punctuation += row_counters[i + checkLocation.row]*self._petar
                if i + checkLocation.row>0:
                    punctuation += row_counters[i + checkLocation.row-1]*self._petar_voltant
                if i + checkLocation.row < checkShape.height-1:
                    punctuation += row_counters[i + checkLocation.row+1]*self._petar_voltant
            else:
                punctuation += row_counters[i + checkLocation.row]*self._casi_petar
        
        for i in range(checkShape.width):
            if column_counters[i + checkLocation.column] == self._board.get_shape().height-checkShape.height:
                punctuation += column_counters[i + checkLocation.column]*self._petar
                if i + checkLocation.column>0:
                    punctuation += column_counters[i + checkLocation.column-1]*self._petar_voltant
                if i + checkLocation.column < checkShape.width-1:
                    punctuation += column_counters[i + checkLocation.column+1]*self._petar_voltant
            else:
                punctuation += column_counters[i + checkLocation.column]*self._casi_petar
        
        
        return punctuation



def play_game(player, blocks, show=True):
    """It plays the blocks puzzle using a pre-defined player. If show is asserted, the state of the player 
    is printed after placing each block. It returns the number of blocks that could be placed.
    """
    if show: print(player)
    count = 0
    for block in blocks:
        assert player.is_legal(block)
        loc = player.play(block)
        if loc is None: break
        player.place_block(loc, block)
        count += 1
        if show: print(player)
    return count


import urllib.request

def read_file(file, url=True):
    """It reads a file of integers representing shapes. Each pair of consecutive integers represents
    a shape (width and height). It returns a list of shapes. If url is not asserted, file is assumed
    to be the name of a local file.
    """
    if url:
        with urllib.request.urlopen(file) as reader:
            items = reader.read().split()
    else:
        with open(file) as reader:
            items = reader.read().split()
            
    # Check there is an even number of items
    assert len(items) % 2 == 0, "Wrong number of items in " + file
    
    # Convert pairs of items to shapes, checking that the items are correct.
    R = []
    for i in range(0, len(items), 2):
        # Check the items are numbers
        assert items[i].isdigit() and items[i+1].isdigit(), "Some element in the list is not an integer"
        w, h = int(items[i]), int(items[i+1])
        assert w > 0 and h > 0, "Illegal size for a shape"
        R.append(Shape(w, h))
    return R
