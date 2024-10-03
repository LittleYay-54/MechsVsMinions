import numpy as np
from numpy import ndarray
from typing import Self

class CVec:
    """
    2x1 Column Vectors that represent positions on the board.
    They are technically mutable, but when CVecs are added, a new CVec is returned,
    which should help avoid issues later
    """

    def __init__(self, pos: tuple[int, int] | list[int] | ndarray[int] | Self) -> None:
        """
        Creates a column vector with the designated 'position' (x_val and y_val)
        :param pos: an appropriately sized data type -- 2x1 tuple, list, ndarray, even another CVec
        """
        # this makes it so that during matrix multiplication (for rotation), this class has priority
        # i.e., this class's __rmatmul__ method is called rather than the ndarray's __matmul__
        self.__array_priority__ = 10
        if isinstance(pos, CVec):
            # creating a new vector to avoid referencing the same object in memory
            self.vector = pos.vector.copy()
            return
        elif len(pos) != 2:
            raise ValueError("pos must be a 2-element tuple or list")
        self.vector = np.array(pos, dtype=int).reshape((2, 1))

    def __getitem__(self, index: int) -> int:
        """
        Allows indexing directly onto the CVec
        :param index: 0 or 1
        :return: x_val if 0, y_val if 1
        """
        if index not in (0, 1):
            raise ValueError("index must be 0 or 1")
        return self.vector[index, 0]

    def __repr__(self) -> str:
        """
        Called when print() is used on the CVec
        :return: a string that represents the CVec (but flattened into a '1D shape' for readability)
        """
        return f"CVec({self.vector.flatten()})"

    def __add__(self, other: Self | ndarray[int]) -> Self:
        """
        Allows addition with other CVecs or 2x1 ndarrays
        :param other: a CVec or a 2x1 ndarray
        :return: the 'sum' as a CVec
        """
        if isinstance(other, CVec):
            return CVec(self.vector + other.vector)
        elif isinstance(other, ndarray):
            return CVec(self.vector + CVec(other).vector)
        else:
            raise TypeError("CVecs can only be added to other CVecs or appropriately sized ndarrays")

    def __mul__(self, other: int) -> Self:
        """
        Allows scalar multiplication
        :param other: int
        :return: the 'scalar product' as a CVec
        """
        if isinstance(other, int):
            return CVec(self.vector * other)
        else:
            raise TypeError("CVecs can only be multiplied by integers")

    def __rmatmul__(self, matrix: ndarray[int]) -> Self:
        """
        Allows matrix multiplication between a 2x2 ndarray and a CVec --
        the CVec must be on the right side of the @ operator
        :param matrix: a 2x2 ndarray
        :return: the result of the 'matrix product' as a CVec
        """
        # Note: this only works properly because CVecs have a higher '__array_priority__'
        if isinstance(matrix, ndarray) and matrix.shape == (2, 2):
            return CVec(np.dot(matrix, self.vector))
        else:
            raise TypeError("matrix must be an ndarray of shape (2, 2)")

    def to_tuple(self) -> tuple[int, int]:
        """
        Returns a length 2 tuple containing the x_val and y_val stored in the CVec --
        useful for indexing other ndarrays
        :return: a tuple in the form of (x_val, y_val)
        """
        x_val = self.vector[0][0]
        y_val = self.vector[1][0]
        return x_val, y_val


class TwoXN:
    """
    Mathematically a matrix of shape (2, N) -- the result of horizontally stacking CVecs
    """

    def __init__(self, matrix: list[CVec] | list[list[int]] | list[tuple[int, int]] | list[ndarray[int]] | ndarray[int]) -> None:
        """
        Creates the matrix with 2xN sized data type
        :param matrix: either a (1D) list of CVec objects or (2D) list of coordinate pairs (either as lists or tuples),
        or an ndarray of shape (2, N)
        """
        if isinstance(matrix, list):
            self.matrix = np.zeros((2, len(matrix)), dtype=int)
            for i in range(len(matrix)):
                self.matrix[:, i] = CVec(matrix[i]).vector.reshape(2,)
        elif isinstance(matrix, ndarray):
            # creating a copy to avoid referencing the same object in memory
            self.matrix = matrix.copy()

    def __repr__(self):
        """
        Called when print() is used on the TwoXN
        :return: a string that represents the TwoXN
        """
        return f"TwoXN(\n{self.matrix}\n)"


def rotate(original: CVec, angle: int) -> CVec:
    """
    Rotates a column vector some right angle counterclockwise about the origin, returning a new one (unless there was no rotation)
    :param original: original CVec
    :param angle: -360, -270, -180, -90, 0, 90, 180, 270, or 360 (degrees)
    :return: new CVec
    """
    if angle == 90 or angle == -270:
        rotation_matrix = np.array([[0, -1], [1, 0]])
    elif angle == 180 or angle == -180:
        rotation_matrix = np.array([[-1, 0], [0, -1]])
    elif angle == 270 or angle == -90:
        rotation_matrix = np.array([[0, 1], [-1, 0]])
    elif angle == 360 or angle == 0 or angle == -360:
        rotation_matrix = np.array([[1, 0], [0, 1]])
    else:
        raise ValueError("angle must be a right angle of integer degrees between -360 and 360")
    # only works because of the __array_priority__ of CVec in the __init__
    # np.matmul(rotation_matrix, original) doesn't seem to work regardless
    return rotation_matrix @ original
