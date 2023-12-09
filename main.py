# noinspection PyTypeChecker

class CrossZeros(object):
    """docstring"""

    def __init__(self, field_size):
        """Constructor"""
        self.field = [[None for _ in range(0, field_size)] for _ in range(0, field_size)]
        self.field_size = field_size
        self.step = 0
        self.winner = None

    def cross(self, row, col):
        if all(0 <= i < self.field_size for i in [row, col]):
            if self.field[row][col] is None:
                # noinspection PyTypeChecker
                self.field[row][col] = 1
                self.field_expansion(row, col)
                return 1
        return 0

    def zero(self, row, col):
        if all(0 <= i < self.field_size for i in [row, col]):
            if self.field[row][col] is None:
                self.field[row][col] = 0
                self.field_expansion(row, col)
                return 1
        return 0

    def win_condition(self):
        for i in range(0, self.field_size):
            for j in range(0, self.field_size):
                horizontal = self.field[i][j:j + 5] if j+5 < self.field_size else []
                vertical = [self.field[i + k][j] for k in range(5)] if i+5 < self.field_size else []
                diagonal_right = [self.field[i + k][j + k] for k in range(5)] \
                    if i < self.field_size - 5 and j < self.field_size - 5 else []
                diagonal_left = [self.field[i - k][j - k] for k in range(5)] \
                    if i - 5 > 0 and j - 5 > 0 else []
                if any(row == [self.step % 2] * 5 for row in [horizontal, vertical, diagonal_left, diagonal_right]):
                    self.winner = self.step % 2
                    return 1

    def game_step(self):
        self.step += 1
        print(f'Step {self.step}\nEnter a row and a column: ')
        if self.step % 2:
            while not self.cross(*(map(int, input().split()))):
                continue
        else:
            while not self.zero(*(map(int, input().split()))):
                continue
        self.display_field()
        if self.win_condition():
            return 0
        # self.field_expansion()
        return 1

    def display_field(self):
        print(self.field_size)
        for row in self.field:
            for col in row:
                match col:
                    case None:
                        print("_ ", end='')
                    case 0:
                        print("o ", end='')
                    case 1:
                        print("x ", end='')
            print()

    def field_expansion(self, row, col):
        expansion_condition = 3  # the number of cells up to the border
        bottom_distance = self.field_size - row - 1  # delete -1 if numerate from 1
        right_distance = self.field_size - col - 1  # delete -1 if numerate from 1
        upper_distance = row  # append -1 if numerate from 1
        left_distance = col  # append -1 if numerate from 1

        if bottom_distance <= 3 and right_distance <= 3:
            bottom_distance = min(bottom_distance, right_distance)
            right_distance = min(bottom_distance, right_distance)
        elif bottom_distance <= 3 and left_distance <= 3:
            bottom_distance = min(bottom_distance, left_distance)
            left_distance = min(bottom_distance, left_distance)
        elif upper_distance <= 3 and right_distance <= 3:
            upper_distance = min(upper_distance, right_distance)
            right_distance = min(upper_distance, right_distance)
        elif upper_distance <= 3 and left_distance <= 3:
            upper_distance = min(upper_distance, left_distance)
            left_distance = min(upper_distance, left_distance)
        elif upper_distance <= 3:
            left_distance = upper_distance
        elif left_distance <= 3:
            upper_distance = left_distance
        elif bottom_distance <= 3:
            right_distance = bottom_distance
        elif right_distance <= 3:
            bottom_distance = right_distance
        else:
            return

        if expansion_condition - right_distance > 0:
            for i in range(self.field_size):
                self.field[i] += [None] * (expansion_condition - right_distance)
        if expansion_condition - left_distance > 0:
            for i in self.field:
                for _ in range(expansion_condition - left_distance):
                    i.insert(0, None)
        # increasing field_size to add the correct lists
        self.field_size += (expansion_condition - min(bottom_distance, right_distance, upper_distance, left_distance))

        for _ in range(expansion_condition - upper_distance):
            self.field.insert(0, [None] * self.field_size)
        for _ in range(expansion_condition - bottom_distance):
            self.field.append([None] * self.field_size)


if __name__ == "__main__":
    gameSession = CrossZeros(10)
    while gameSession.game_step():
        print(gameSession.game_step())
    print(gameSession.winner)
