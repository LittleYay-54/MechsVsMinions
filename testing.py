import numpy as np

new_array = np.array([1, 2])
print(new_array.shape)
print(new_array.shape == (2))
print(new_array.shape == (2,))

# ok I'm confused


from typing import NewType, Annotated
greeting = Annotated[str, "Welcome Message"]
a: greeting = "Hello"
print(greeting)
