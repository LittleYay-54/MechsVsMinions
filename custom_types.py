import numpy as np
from numpy.typing import NDArray
from typing import NewType, Annotated

# After searching for 20 minutes, I have failed to remember the explicit reason I had that
# I was using to justify the Vectors being of shape (2, 1).
# Fine, I'll give in, Vectors will just be of shape (2,).

# Vectors are NDArrays of shape (2,) that are intended to represent (x, y) coordinates
# for the purposes of location, orientation, etc.
# for example, np.array([1, 0]) represents the "right" orientation,
# while np.array([0, -1]) represents the "down" direction.
# Due to the row-major default nature of numpy,
# interpret Vectors as "pointing down", i.e. column vectors.
Vector = Annotated[NDArray[np.int_], (2,)]
# "Annotated" simply helps you and possibly your IDE see that Vectors
# are supposed to be NDArrays of ints with shape (2,), but it doesn't enforce anything

# Following the new "notation" for Vectors, arrays of Vectors, i.e. "Matrices",
# will also follow the new format.
# They will still be 2D, but instead of being of shape (2, n), they will be
# of shape (n, 2) to emulate the "array of Vectors" notion.
# In other words, these "Matrices" will have 2 columns, with each row being a "Vector".
# Thus, you should visualize the Vectors (which are vertical) as being rotated
# to become horizontal, and then vertically stacked to compose the Matrix.
Matrix = Annotated[NDArray[np.int_], (..., 2)]

# This type will only be used in the board __init__ function type hint:
NDArray2D = Annotated[NDArray[...], (..., ...)]
# Just a 2D NDArray with an arbitrary length and width, and containing any data type.
