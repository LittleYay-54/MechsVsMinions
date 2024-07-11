import itertools

# 1 = right, 2 = down, 3 = left, 4 = up
oil_squares = [[2, 2], [2, 3], [3, 2], [3, 3]]
minions = [[2, 0], [2, 1], [0, 2], [1, 2], [2, 4], [5, 2]]
number = 0

def overflow_check(position):
    if position == 6:
        return position - 1
    if position == -1:
        return position + 1
    else:
        return position


class Tristana:
    def __init__(self, orientation, command_line, location, temp_minions, curr_slot, text, command_to_execute):
        self.orientation = orientation
        self.command_line = command_line
        self.location = location
        self.temp_minions = temp_minions
        self.curr_slot = curr_slot
        self.text = text
        if command_to_execute != None:
            command_to_execute(self)
        self.execute()

    def damage(self, square):
        if square in self.temp_minions:
            self.temp_minions.remove(square)

    def turn(self, way):
        if way == "clockwise":
            self.orientation = (self.orientation % 4) + 1
        elif way == "counterclockwise":
            self.orientation = (self.orientation - 2) % 4 + 1

    def move(self, direction):
        if direction == 1:
            self.location[0] = overflow_check(self.location[0] + 1)
        if direction == 2:
            self.location[1] = overflow_check(self.location[1] - 1)
        if direction == 3:
            self.location[0] = overflow_check(self.location[0] - 1)
        if direction == 4:
            self.location[1] = overflow_check(self.location[1] + 1)

        self.damage(self.location)

        if self.location in oil_squares:
            self.move(direction)


    def blaze(self, level):
        self.move(self.orientation)
        if level == 2:
            self.move(self.orientation)
        if self.orientation in [2, 4]:
            self.damage([self.location[0] + 1, self.location[1]])
            self.damage([self.location[0] - 1, self.location[1]])
        if self.orientation in [1, 3]:
            self.damage([self.location[0], self.location[1] + 1])
            self.damage([self.location[0], self.location[1] - 1])
        self.text += f"Blaze[{level}] "

    def cyclotron(self, level):
        self.damage([self.location[0] + 1, self.location[1] + 1])
        self.damage([self.location[0] + 1, self.location[1] - 1])
        self.damage([self.location[0] - 1, self.location[1] + 1])
        self.damage([self.location[0] - 1, self.location[1] - 1])
        if level == 2:
            self.damage([self.location[0] + 2, self.location[1] + 2])
            self.damage([self.location[0] + 2, self.location[1] - 2])
            self.damage([self.location[0] - 2, self.location[1] + 2])
            self.damage([self.location[0] - 2, self.location[1] - 2])

        # choose either clockwise or counterclockwise
        anon = lambda x: x.turn("clockwise")
        Tristana(self.orientation, self.command_line, self.location.copy(), self.temp_minions.copy(), self.curr_slot + 1, self.text + f"Cyclotron[{level}] (Clockwise) ", anon)
        anon = lambda x: x.turn("counterclockwise")
        Tristana(self.orientation, self.command_line, self.location.copy(), self.temp_minions.copy(), self.curr_slot + 1, self.text + f"Cyclotron[{level}] (Counter-Clockwise) ", anon)
        if level == 2:
            anon = lambda x: (x.turn("clockwise"), x.turn("clockwise"))
            Tristana(self.orientation, self.command_line, self.location.copy(), self.temp_minions.copy(), self.curr_slot + 1,
                     self.text + f"Cyclotron[{level}] (Full Spin)", anon)

    def flamespitter(self, level):
        if self.orientation == 1:
            self.damage([self.location[0] + 1, self.location[1]])
            self.damage([self.location[0] + 2, self.location[1]])
            if level == 2:
                self.damage([self.location[0] + 2, self.location[1] + 1])
                self.damage([self.location[0] + 2, self.location[1] - 1])
        if self.orientation == 2:
            self.damage([self.location[0], self.location[1] - 1])
            self.damage([self.location[0], self.location[1] - 2])
            if level == 2:
                self.damage([self.location[0] + 1, self.location[1] - 1])
                self.damage([self.location[0] - 1, self.location[1] - 2])
        if self.orientation == 3:
            self.damage([self.location[0] - 1, self.location[1]])
            self.damage([self.location[0] - 2, self.location[1]])
            if level == 2:
                self.damage([self.location[0] - 2, self.location[1] + 1])
                self.damage([self.location[0] - 2, self.location[1] - 1])
        if self.orientation == 4:
            self.damage([self.location[0], self.location[1] + 1])
            self.damage([self.location[0], self.location[1] + 2])
            if level == 2:
                self.damage([self.location[0] + 1, self.location[1] + 1])
                self.damage([self.location[0] - 1, self.location[1] + 2])
        self.text += f"Flamespitter[{level}] "

    def omnistomp(self, level):
        left = (self.orientation - 2) % 4 + 1
        right = (self.orientation % 4) + 1
        forward = self.orientation
        if level == 1:
            anon = lambda x: x.move(left)
            Tristana(self.orientation, self.command_line, self.location.copy(), self.temp_minions.copy(), self.curr_slot + 1,
                     self.text + f"Omnistomp[{level}] (Left) ", anon)
            anon = lambda x: x.move(forward)
            Tristana(self.orientation, self.command_line, self.location.copy(), self.temp_minions.copy(), self.curr_slot + 1,
                     self.text + f"Omnistomp[{level}] (Forward) ", anon)
            anon = lambda x: x.move(right)
            Tristana(self.orientation, self.command_line, self.location.copy(), self.temp_minions.copy(), self.curr_slot + 1,
                     self.text + f"Omnistomp[{level}] (Right) ", anon)
        if level == 2:
            anon = lambda x: (x.move(left), x.move(left))
            Tristana(self.orientation, self.command_line, self.location.copy(), self.temp_minions.copy(), self.curr_slot + 1,
                     self.text + f"Omnistomp[{level}] (Left) ", anon)
            anon = lambda x: (x.move(forward), x.move(forward))
            Tristana(self.orientation, self.command_line, self.location.copy(), self.temp_minions.copy(), self.curr_slot + 1,
                     self.text + f"Omnistomp[{level}] (Forward) ", anon)
            anon = lambda x: (x.move(right), x.move(right))
            Tristana(self.orientation, self.command_line, self.location.copy(), self.temp_minions.copy(), self.curr_slot + 1,
                     self.text + f"Omnistomp[{level}] (Right) ", anon)

    def skewer(self, level):
        self.move(self.orientation)
        if level == 2:
            self.move(self.orientation)
        self.text += f"Skewer[{level}] "

    def speed(self, level):
        if level == 1:
            anon = lambda x: x.move(x.orientation)
            Tristana(self.orientation, self.command_line, self.location.copy(), self.temp_minions.copy(), self.curr_slot + 1,
                     self.text + f"Speed[{level}] (1 Square) ", anon)
            anon = lambda x: (x.move(x.orientation), x.move(x.orientation))
            Tristana(self.orientation, self.command_line, self.location.copy(), self.temp_minions.copy(), self.curr_slot + 1,
                     self.text + f"Speed[{level}] (2 Squares) ", anon)
        if level == 2:
            anon = lambda x: (x.move(x.orientation), x.move(x.orientation))
            Tristana(self.orientation, self.command_line, self.location.copy(), self.temp_minions.copy(), self.curr_slot + 1,
                     self.text + f"Speed[{level}] (2 Squares) ", anon)
            anon = lambda x: (x.move(x.orientation), x.move(x.orientation), x.move(x.orientation))
            Tristana(self.orientation, self.command_line, self.location.copy(), self.temp_minions.copy(), self.curr_slot + 1,
                     self.text + f"Speed[{level}] (3 Squares) ", anon)
            anon = lambda x: (x.move(x.orientation), x.move(x.orientation), x.move(x.orientation), x.move(x.orientation))
            Tristana(self.orientation, self.command_line, self.location.copy(), self.temp_minions.copy(), self.curr_slot + 1,
                     self.text + f"Speed[{level}] (4 Squares) ", anon)

    def execute(self):
        if self.curr_slot == 7:
            if not self.temp_minions:
                print(f"This is a winning command line: {self.text}")
            return
        command = self.command_line[self.curr_slot - 1]
        if command == "b":
            self.blaze(1)
        elif command == "B":
            self.blaze(2)
        elif command == "c":
            self.cyclotron(1)
        elif command == "C":
            self.cyclotron(2)
        elif command == "f":
            self.flamespitter(1)
        elif command == "F":
            self.flamespitter(2)
        elif command == "o":
            self.omnistomp(1)
        elif command == "O":
            self.omnistomp(2)
        elif command == "sk":
            self.skewer(1)
        elif command == "SK":
            self.skewer(2)
        elif command == "sp":
            self.speed(1)
        elif command == "SP":
            self.speed(2)
        self.curr_slot += 1
        if command in ["o", "O", "c", "C", "sp", "SP"]:
            return
        # if self.curr_slot < 7:
            # print(f"Call number: BLANK, number of minions remaining: {len(self.temp_minions)}, locations of the minions: {self.temp_minions}, Commands executed so far: {self.text}")
        self.execute()


basis_1 = ["b", "c", "f", "o", "sk", "sp"]
basis_2 = ["b", "c", "f", "O", "sk", "sp"]
basis_3 = ["b", "c", "f", "o", "o", "s"]
basis_4 = ["b", "c", "f", "o", "sk", "o"]
basis_5 = ["b", "c", "o", "o", "sk", "sp"]
basis_6 = ["b", "o", "f", "o", "sk", "sp"]
basis_7 = ["o", "c", "f", "o", "sk", "sp"]
basis_8 = ["b", "C", "f", "o", "sk", "o"]
basis_9 = ["B", "c", "o", "o", "sk", "sp"]
basis_10 = ["b", "o", "f", "o", "sk", "SP"]
basis_11 = ["b", "o", "F", "o", "sk", "sp"]
bases = [basis_1, basis_2, basis_3, basis_4, basis_5, basis_6, basis_7, basis_8, basis_9, basis_10, basis_11]

def permutation_generator():
    running_list = []
    for basis in bases:
        running_list += itertools.permutations(basis)
    for command_line in running_list:
        for orientation in [1, 2, 3, 4]:
            temp_string_dict = {1: "Right", 2: "Down", 3: "Left", 4: "Up"}
            Tristana(orientation, command_line, [4, 4], minions.copy(), 1,
                     f"Facing Direction: {temp_string_dict[orientation]}, ", None)

permutation_generator()
