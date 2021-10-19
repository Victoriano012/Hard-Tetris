import collections

Location = collections.namedtuple('Location', 'row column')
Shape = collections.namedtuple('Shape', 'width height')

class GameBoard:
    """
    Class to create and manipulate the boards of the game.
    """
    
    def __init__(self, myShape):
        """
        Initialization of the board with a given shape.
        Arguments:
            myShape -> shape of the board
        Preconditions:
            myShape must be a valid Shape
        """
        
        # Checking that myShape is a valid Shape
        if not isinstance(myShape, Shape):
            raise Exception("The argument is not a shape")
        if not isinstance(myShape.width, int) or not isinstance(myShape.height, int):
            raise Exception("The shape is not valid")
        if myShape.width <= 0 or myShape.height <= 0:
            raise Exception("The shape is not valid")
        
        # Creation of the board, a width*height matrix of booleans
        # All booleans begin at false, they are all empty
        self._board = []
        for j in range(myShape.height):
            row = []
            for i in range(myShape.width):
                row.append(False)
            self._board.append(row)
        
        # initialitzation of all other attributes
        self._shape = myShape
        self._row_counters = [0]*myShape.height
        self._column_counters = [0]*myShape.width
     
    
    def __str__(self):
        """
        Creation of the string to be printed when printing a GameBoard
        """
        
        s = ''
        # for all squares of the board, add its state
        for i in range(self.get_shape().height-1, -1, -1):
            for j in range(self.get_shape().width):
                if not self._board[i][j]:
                    s += '\u2b1c' # full square
                else:
                    s += '\u2b1b' # empty square
            s += '\n'
        return s
    
    
    def __repr__(self):
        
        s = str(self.get_shape().width) + 'x' + str(self.get_shape().height) + ' board: {'
        
        # for all squares, add it to the list if it's full
        coma = False
        for i in range(self.get_shape().height):
            for j in range(self.get_shape().width):
                if self._board[i][j]:
                    if coma:
                        s += ', '
                    else:
                        coma = True
                    s += '(' + str(i) + ', ' + str(j) + ')'
        s += '}'
        
        return s
    
    
    def get_shape(self):
        return self._shape
    
    def row_counters(self):
        return self._row_counters
    
    def column_counters(self):
        return self._column_counters

    def full_rows(self):
        """
        Method to get all full rows of the board.
        """
        
        full = []
        for i in range(self.get_shape().height):
            if self._row_counters[i] == self.get_shape().width:
                full.append(i)
        return full
    
    
    def full_columns(self):
        """
        Method to get all full columns of the board.
        """
        
        full = []
        for i in range(self.get_shape().width):
            if self._column_counters[i] == self.get_shape().height:
                full.append(i)
        return full
    
    
    def _are_valid_Shape_and_Location(self, checkLocation, checkShape):
        """
        Auxiliar method to check if a Shape and a Location are valid for this board
        """
        
        # checking they are actually a Shape and a Location
        if not isinstance(checkShape, Shape):
            return "The shape is not a shape"
        if not isinstance(checkShape.width, int) or not isinstance(checkShape.height, int):
            return "The shape is not a valid shape"
        if not isinstance(checkLocation, Location):
            return "The location is not a location"
        if not isinstance(checkLocation.row, int) or not isinstance(checkLocation.column, int):
            return "The location is not a valid location"
        
        # checking they are not out of bounds
        if checkLocation.row < 0 or checkLocation.column < 0:
            return "You are out of bounds"
        if checkLocation.row + checkShape.height > self.get_shape().height:
            return "You are out of bounds"
        if checkLocation.column + checkShape.width > self.get_shape().width:
            return "You are out of bounds"

        return "Fine"
        
    
    def is_empty(self, checkLocation, checkShape = Shape(1, 1)):
        """
        Method to check if a rectangle is empty. If no shape is given, the rectangle is 1x1, a square.
        Arguments:
            checkLocation -> The location of bottom left square of the rectangle
            checkShape -> The shape of the rectangle, optional argument
        Preconditions:
            checkLocation and checkShape are a valid location and shape, respectively
        """
        
        # checking that checkLocation and checkShape are valid
        s = self._are_valid_Shape_and_Location(checkLocation, checkShape)
        if s != "Fine":
            raise Exception(s)
        
        # for each square in the rectangle, if it is full the rectangle is not empty
        for i in range(checkLocation.row, checkLocation.row + checkShape.height):
            for j in range(checkLocation.column, checkLocation.column + checkShape.width):
                if self._board[i][j]:
                    return False
        
        return True
    
    def is_full(self, checkLocation, checkShape = Shape(1, 1)):
        """
        Method to check if a rectangle is full. If no shape is given, the rectangle is 1x1, a square.
        Arguments:
            checkLocation -> The location of bottom left square of the rectangle
            checkShape -> The shape of the rectangle, optional argument
        Preconditions:
            checkLocation and checkShape are a valid location and shape, respectively
        """
        
        # checking that checkLocation and checkShape are valid
        s = self._are_valid_Shape_and_Location(checkLocation, checkShape)
        if s != "Fine":
            raise Exception(s)
        
        # for each square in the rectangle, if it is empty the rectangle is not full
        for i in range(checkLocation.row, checkLocation.row + checkShape.height):
            for j in range(checkLocation.column, checkLocation.column + checkShape.width):
                if not self._board[i][j]:
                    return False
        
        return True
    
    def clear_rows(self, clearRows):
        """
        Method to clear the specified rows
        Arguments:
            clearRows -> An array of all rows to be cleared
        """
        
        # set their counters to 0
        for i in clearRows:
            self._row_counters[i] = 0
        
        # clear the squares and change the column counters
        for i in clearRows:
            for j in range(self.get_shape().width):
                if self._board[i][j]:
                    self._column_counters[j] -= 1
                    self._board[i][j] = False
                    
        return self
    
    def clear_columns(self, clearColumns):
        """
        Method to clear the specified columns
        Arguments:
            clearColumns -> An array of all columns to be cleared
        """
        
        # set their counters to 0
        for i in clearColumns:
            self._column_counters[i] = 0
            
        # clear the squares and change the row counters
        for i in range(self.get_shape().height):
            for j in clearColumns:
                if self._board[i][j]:
                    self._row_counters[i] -= 1
                    self._board[i][j] = False
                    
        return self
        
    
    def put(self, putLocation, putShape = Shape(1, 1)):
        """
        Method to put a rectangle. If no shape is given, the rectangle is 1x1, a square.
        Arguments:
            putLocation -> The location of bottom left square of the rectangle
            putShape -> The shape of the rectangle, optional argument
        Preconditions:
            putLocation and putShape are a valid location and shape, respectively
            The rectangle is to be put at an empty spot
        """
        
        # checking if the arguments are valid
        try:
            if not self.is_empty(putLocation, putShape):
                raise Exception("What you want to fill is not empty")
        except Exception as ex:
            # the location or the shape are not valid
            raise ex
        
        # actualize the squares of the board
        for i in range(putLocation.row, putLocation.row + putShape.height):
            for j in range(putLocation.column, putLocation.column + putShape.width):
                self._board[i][j] = True
        
        # actualize the modified counters
        for i in range(putLocation.row, putLocation.row + putShape.height):
            self._row_counters[i] += putShape.width
        for j in range(putLocation.column, putLocation.column + putShape.width):
            self._column_counters[j] += putShape.height
        
        return self
    
    
    def remove(self, removeLocation, removeShape = Shape(1, 1)):
        """
        Method to remove a rectangle. If no shape is given, the rectangle is 1x1, a square.
        Arguments:
            removeLocation -> The location of bottom left square of the rectangle
            removeShape -> The shape of the rectangle, optional argument
        Preconditions:
            removeLocation and removeShape are a valid location and shape, respectively
            The rectangle to be removed is full
        """
        
        # checking if the arguments are valid
        try:
            if not self.is_full(removeLocation, removeShape):
                raise Exception("What you want to remove is not full")
        except Exception as ex:
            # the location or the shape are not valid
            raise ex
        
        # actualize the squares of the board
        for i in range(removeLocation.row, removeLocation.row + removeShape.height):
            for j in range(removeLocation.column, removeLocation.column + removeShape.width):
                self._board[i][j] = False
        
        # actualize the modified counters
        for i in range(removeLocation.row, removeLocation.row + removeShape.height):
            self._row_counters[i] -= removeShape.width
        for j in range(removeLocation.column, removeLocation.column + removeShape.width):
            self._column_counters[j] -= removeShape.height
        
        return self
