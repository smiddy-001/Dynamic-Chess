class PieceMovements(list):
    def __repr__(self):
        return self._data

    def __str__(self):
        return f"{self.name:<16}" + ": " + str(self.__repr__())

    def __init__(self, name):
        self._data = []
        self.name = name

    def relative(self, rel_x, rel_y):
        # 1 in the positive is ^ for white and down for black
        vertex = ("r", rel_x, rel_y)  # r for relative
        self._data.append(vertex)

    def relative_not_in_danger(self, rel_x, rel_y):
        # 1 in the positive is ^ for white and down for black
        vertex = ("s", rel_x, rel_y)  # s for safe
        self._data.append(vertex)

    def only_if_enemy_piece_there(self, rel_x, rel_y):
        # for pawns mostly
        vertex = ("e", rel_x, rel_y)  # e for enemy
        self._data.append(vertex)

    def only_on_first_touch(self, rel_x, rel_y):
        # for pawns mostly
        vertex = ("f", rel_x, rel_y)  # f for first
        self._data.append(vertex)

    def absolute(self, is_x: bool, is_y: bool):
        vertex = ("a", is_x, is_y)  # a for absolute( horizontal / vertical )
        self._data.append(vertex)

    def diagonal(self, is_bl_to_tr, is_br_to_tl):
        vertex = ("d", is_bl_to_tr, is_br_to_tl)  # d for diagonal ( / and \ )
        self._data.append(vertex)

    def get_loc_of_type(self, type_value):
        # == OPTIMISATION ==
        # could be a hash table look-up
        result = []
        for item in self._data:  # look for item
            if item[0] == type_value:
                result.append(item[1:])
        return result

    def has_loc_of_type(self, type_value):
        # == OPTIMISATION ==
        # could be a hash table look-up
        result = []
        for item in self._data:  # look for item
            if item[0] == type_value:
                result.append(item[1:])
        return result

    def only_hidden(self):
        self._data.append("see hidden")
        return

    def only_empty(self):
        self._data.append("see empty")
        return

    def add_manually(self, moves):
        self._data.append()

    def remove_particular_move(self, move):
        i = 0
        popped = set()
        while move in self._data:
            if self._data[i] == move:
                popped.add(self._data.pop(i))
        print("removed:", {*popped})


pawn = PieceMovements("pawn")
# as pawns can only move forwards
pawn.relative(0, 1)
pawn.only_on_first_touch(0, 2)  # pawns can go 2 on first touch
pawn.only_if_enemy_piece_there(1, 1)  # up
pawn.only_if_enemy_piece_there(-1, 0)  # diagonal only if it can take a piece

knight = PieceMovements("knight")
knight.relative(1, 2)  # right, top, top
knight.relative(2, 1)  # right, right, top
knight.relative(-1, 2)  # left, top, top
knight.relative(-2, 1)  # left, left, top
knight.relative(1, -2)  # right, bottom, bottom
knight.relative(2, -1)  # right, right, bottom
knight.relative(-1, -2)  # left, bottom, bottom
knight.relative(-2, -1)  # left, left, bottom

rook = PieceMovements("rook")
rook.absolute(True, True)  # horizontal / vertical

bishop = PieceMovements("bishop")
bishop.diagonal(True, True)  # diagonal

queen = PieceMovements("queen")
queen.diagonal(True, True)  # diagonal
queen.absolute(True, True)  # horizontal / vertical

king = PieceMovements("king")
king.relative_not_in_danger(0, 1)  # top
king.relative_not_in_danger(1, 1)  # top right
king.relative_not_in_danger(1, 0)  # right
king.relative_not_in_danger(1, 0)  # bottom right
king.relative_not_in_danger(0, -1)  # bottom
king.relative_not_in_danger(-1, -1)  # bottom left
king.relative_not_in_danger(-1, 0)  # left
king.relative_not_in_danger(-1, 1)  # top left

wizard = PieceMovements("wizard")
wizard.only_hidden()
wizard.only_empty()

if __name__ == "__main__":
    pass
