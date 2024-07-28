from itertools import combinations
from typing import Callable
import numpy as np

def a(num: int, c: bool):
    def b():
        if c:
            print(num+1)
        else:
            print(num-1)

    return b


p = a(6, False)
p()

for i in range(-3, 3):
    print(i)


x = 15
if x > 10:
    y = 5

print(y)

strings = ['a', 'b']
u = combinations(strings, 2)
print(u)
print(list(u))
for item in u:
    print(item)


def recursion_test(some_list, depth):
    if depth > 6:
        return some_list
    else:
        some_list = some_list + [0]
        return recursion_test(some_list, depth+1)


b = [1]
print(recursion_test(b, 0))
print(b)

# n = ([1, 2], [2, 1], [1, 2], [2])
#
# for i in range(3):
#     b = int(input("Pick an Index (0-3):"))
#     print(n[b])


class Dog:
    def __init__(self, name: str, age: int) -> None:
        self.name: str = name
        self.age: int = age

    def bark(self) -> None:
        print(self.name)

    def future_bark(self) -> Callable[[], None]:
        def func():
            self.bark()
        return func


for name, age in zip(['Bob', 'Alice', 'Carl'], [1, 2, 3]):
    dog = Dog(name, age)
    b = Dog.future_bark(dog)
    b()




billy = 6


def modify_billy():
    global billy
    billy = 7


print(billy)
modify_billy()
print(billy)


# q = np.array([1, 2])
# w = np.array([2, 3])
#
# temp_arr = [q, w]
# print(np.array([2, 4]) in temp_arr)

new_arr = np.array([5, 8])
new_arr_2 = new_arr + [1, 1]
new_arr_2 += [1, 1]
print(new_arr_2)
print(new_arr)

def append_to_list(target_list, element):
    target_list.append(element)

new_list = []
append_to_list(new_list, 15)
print(new_list)

print(np.array((94, 44)))

q = [1, 2]
w = q

