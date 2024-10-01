import numpy as np
from numpy import ndarray
from typing import Self

class CVec:
    """2x1 Column Vectors that represent positions on the board.
    They are technically mutable, but when CVecs are added, a new CVec is returned,
    which should help avoid issues later"""

    def __init__(self, pos: tuple[int, int] | list[int] | ndarray[int] | Self) -> None:
        """initialize with an x_val and y_val stored in either a tuple, list, ndarray, or CVec itself"""
        if isinstance(pos, CVec):
            # creating a new vector to avoid referencing the same object in memory
            self.vector = pos.vector.copy()
        elif len(pos) != 2:
            raise ValueError("pos must be a 2-element tuple or list")
        self.vector = np.array(pos).reshape(2, 1)

    def __getitem__(self, index: int) -> int:
        """Allows indexing directly onto the CVec: 0 = x_val, 1 = y_val"""
        if index not in (0, 1):
            raise ValueError("index must be 0 or 1")
        return self.vector[index, 0]

    def __repr__(self) -> str:
        """Prints the CVec but as a 1D array"""
        return f"CVec({self.vector.flatten()})"

    def __add__(self, other: Self | ndarray[int]) -> Self:
        """Allows addition of CVecs with other CVecs or appropriately sized ndarrays"""
        if isinstance(other, CVec):
            return CVec(self.vector + other.vector)
        elif isinstance(other, ndarray):
            return CVec(self.vector + CVec(other).vector)
        else:
            raise TypeError("CVecs can only be added to other CVecs or appropriately sized ndarrays")

    def __sub__(self, other: Self | ndarray[int]) -> Self:
        """Allows addition of CVecs with other CVecs or appropriately sized ndarrays"""
        if isinstance(other, CVec):
            return CVec(self.vector - other.vector)
        elif isinstance(other, ndarray):
            return CVec(self.vector - CVec(other).vector)
        else:
            raise TypeError("CVecs can only be subtracted by other CVecs or appropriately sized ndarrays")

    def __rmatmul__(self, matrix: ndarray[int]) -> Self:
        """Allows matrix multiplication between a 2x2 ndarray and a CVec --
        the CVec must be on the right of the @ operator"""
        if isinstance(matrix, ndarray) and matrix.shape == (2, 2):
            return CVec(np.dot(matrix, self.vector))
        else:
            raise TypeError("matrix must be an ndarray of shape (2, 2)")

    def to_tuple(self) -> tuple[int, int]:
        """Returns a length 2 tuple containing the x_val and y_val stored in the CVec --
        useful for indexing other ndarrays"""
        x_val = self.vector[0][0]
        y_val = self.vector[1][0]
        return x_val, y_val


class TwoXN:
    """Mathematically a matrix of shape (2, N) -- the result of horizontally stacking CVecs"""

    def __init__(self, matrix: list[CVec] | list[list[int]] | list[tuple[int, int]] | list[ndarray[int]] | ndarray[int]) -> None:
        """Initialize with either a list of CVec objects or coordinate pairs, or an ndarray of shape (2, N)"""
        if isinstance(matrix, list):
            self.matrix = np.zeros((2, len(matrix)), dtype=int)
            for i in range(len(matrix)):
                self.matrix[:, i] = CVec(matrix[i]).vector.reshape(2,)
        elif isinstance(matrix, ndarray):
            # creating a copy to avoid referencing the same object in memory
            self.matrix = matrix.copy()

    def __repr__(self):
        """Prints the underlying 2xN ndarray"""
        return f"TwoXN(\n{self.matrix}\n)"







