import time
from basislists import generate


def timer(func):
    def wrapper(*args):
        start_time = time.time()
        for i in range(100_000):
            func(*args)
        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f"Executing {func} 100,000 times costed {elapsed_time} seconds.")

    return wrapper


def do_something():
    return 58 * 94


allowed_cards = ['Blaze', 'Cyclotron', 'Flamespitter', 'Omnistomp', 'Omnistomp', 'Skewer', 'Speed']
basis_lists = generate(allowed_cards, [6])


@timer
def mymethod():
    for basis_list in basis_lists:
        for card in basis_list:
            if card in set(allowed_cards):
                command = card
                do_something()
            else:
                level = int(card[-1])
                command = card[:-1]
                do_something()


@timer
def yourmethod():
    for basis_list in basis_lists:
        for card in basis_list:
            try:
                level = int(card[-1])
                command = card[:-1]
                do_something()
            except ValueError as e:
                command = card
                do_something()


mymethod()
yourmethod()