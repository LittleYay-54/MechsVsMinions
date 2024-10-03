from auxiliary import *

class Tile:
    """
    A space on the board
    It knows whether there's oil on it, a rune space, a wall, etc.
    It also stores whatever 'entity' is occupying it
    """

    def __init__(self, x_pos: int, y_pos: int) -> None:
        """
        Creates a tile with coordinates (x_pos, y_pos)
        :param x_pos: x-coordinate
        :param y_pos: y-coordinate
        """
        self.location = CVec((x_pos, y_pos))
        self.wall: bool = False
        self.oil: bool = False
        # self.entity = None

    def __repr__(self) -> str:
        """
        Called when print() is used on the Tile
        :return: a string represent the contents of the Tile
        """
        char = " "
        if self.wall:
            char = "\u2B1C"  # unicode for white square
        # elif self.entity:
        #     char = self.entity.__repr__()
        elif self.oil:
            char = "o"
        return f"Tile([{char}])"

    # def place_thing

    # def remove_thing


class Board:
    """
    A 2D ndarray of Tiles
    Contains all the things
    """

    def __init__(self, board_space: ndarray) -> None:
        """
        Creates a board object with the same shape as an input ndArray.
        :param board_space: a 2D ndArray of the desired shape -- it doesn't matter what it actually contains
        """
        # Note: creating a vectorized function with np.vectorize() is not actually faster than normal iteration
        # It's just a wrapper for applying a python function to each element in the array,
        # unlike true vectorized functions like np.sin(), np.add(), etc.
        if len(board_space.shape) != 2:
            TypeError("The input array 'boardspace' must be 2D")
        x_size, y_size = board_space.shape
        self.board_space = np.empty((x_size, y_size), dtype=object)
        for i in range(x_size):
            for j in range(y_size):
                self.board_space[i, j] = Tile(i, j)

    def __getitem__(self, index: tuple[int, int]) -> Tile:
        """
        Allows indexing directly onto the Board
        :param index: a tuple of ints representing the coordinates (x_pos, y_pos)
        :return: the Tile object that is stored at that position
        """
        return self.board_space[index]

    def __repr__(self) -> str:
        """
        Called when print() is used on the Board
        :return: a string that represents each Tile (and its contents) on the board
        """
        message = "Board(\n"
        for j in range(self.board_space.shape[1])[::-1]:
            for i in range(self.board_space.shape[0]):
                tile_contents = self[i, j].__repr__()[5:-1]
                message += tile_contents + " "
            message += "\n"
        message += ")"
        return message



