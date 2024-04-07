# CHESS ENGINE (written in python)
# ================================
# Riley Smith - 1st Apr 2024

# INPUTS
# ======
# - user make new game
# - user choose single or two player
# for single player
# ===================
# - user chooses bot thinking level (1-5) where 5 is the number of 'thoughts' the bot will have per piece
# both single / two
# =================
# - get username
# - restart game
# - move piece

# REFERENCES
# ==========
# UML state diagram by Alessandro Scotti from "chessprogramming.org/Chess_Engine_Communication_Protocol"

# IMPORTS
# =======
from piece_setups import PieceMovements

# CONSTANTS
# =========
from icons import CRAB_CHESS_ICONS, NORMAL_CHESS_ICONS
from piece_setups import pawn, knight, rook, bishop, queen, king, wizard

BOARD_TEMPLATE = [
    ["br", "bh", "bb", "bq", "bk", "bb", "bh", "br"],
    ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
    ["--", "--", "--", "--", "--", "--", "--", "--"],
    ["--", "--", "--", "--", "--", "--", "--", "--"],
    ["--", "--", "--", "--", "--", "--", "--", "--"],
    ["--", "--", "--", "--", "--", "--", "--", "--"],
    ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
    ["wr", "wh", "wb", "wk", "wq", "wb", "wh", "wr"]
]

WIZARD_BOARD_TEMPLATE = [
    ["!!", "!!", "!!", "!!", "!!", "!!", "!!", "!!", "!!", "!!", "!!"],
    ["!!", "br", "bh", "bb", "bq", "bw", "bk", "bb", "bh", "br", "!!"],
    ["!!", "bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp", "!!"],
    ["!!", "--", "--", "--", "--", "--", "--", "--", "--", "--", "!!"],
    ["!!", "--", "--", "--", "--", "--", "--", "--", "--", "--", "!!"],
    ["!!", "--", "--", "--", "--", "--", "--", "--", "--", "--", "!!"],
    ["!!", "--", "--", "--", "--", "--", "--", "--", "--", "--", "!!"],
    ["!!", "wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp", "!!"],
    ["!!", "wr", "wh", "wb", "wk", "ww", "wq", "wb", "wh", "wr", "!!"],
    ["!!", "!!", "!!", "!!", "!!", "!!", "!!", "!!", "!!", "!!", "!!"]
]
# hidden values are only used to 'hide' the squares from the gui and the possible moves part of the code
# empty values are used to show a spot if free and a piece can move there if they would like to
EMPTY_ID = "--"
HIDDEN_ID = "!!"
NON_MOVABLE_PIECE_TYPES = {"empty", "hidden"}
PIECES_THAT_REQUIRE_BOARD_INFO = {"wizard"}  # the wizard manipulates the board
COLOR_MAPS = {"!": None, "-": None, "w": "white", "b": "black"}
PIECE_MAPS = {"!": "hidden", "-": "empty", "p": "pawn", "r": "rook", "h": "knight", "b": "bishop", "q": "queen", "k": "king",
              "w": "wizard"}
PLAIN_BOARD_N_OF_PLAYERS = 2
MAX_BOARD = 16

GAME_MODES = {"normal", "wizard"}
GAME_SKINS = {"normal", "crab"}

# global things that can change
# =============================
taken_pieces = []
turns_take = 0
current_player_turn = "player1"
current_game_mode = "normal"  # from


def start_game():
    game_mode = "normal" # in GAME_MODES
    game_skin = "crab" # in GAME_SKINS
    if game_mode == "normal":
        my_game_board = ChessBoard(BOARD_TEMPLATE)
    elif game_mode == "wizard":
        my_game_board = ChessBoard(WIZARD_BOARD_TEMPLATE)

    if game_skin == "normal":
        my_game_skin = NORMAL_CHESS_ICONS
    elif game_skin == "crab":
        my_game_skin = CRAB_CHESS_ICONS

    list_to_show_user = []

    result = []
    i = 0
    for y_val, rows in enumerate(my_game_board.board):
        lil_result = []
        for x_val, cell in enumerate(rows):
            i = y_val % len(my_game_skin["empty"]) + x_val
            if cell.name == "empty":
                variation_icon_size = len(my_game_skin["empty"])
                lil_result.append((list(my_game_skin["empty"])[i % variation_icon_size], generate_piece_id("empty", y_val, x_val)))
            elif cell.name != "hidden":
                lil_result.append((my_game_skin[cell.color][cell.name], generate_piece_id(cell.name, y_val, x_val)))
        result.append(lil_result)
    return result


def generate_piece_id(piece_name, x, y):
    return f"{piece_name}{x}{y}"


class ChessBoard:
    def __init__(self, game_template):
        self.board = []  # Initialize an empty list to hold the board
        for y, row in enumerate(game_template):
            board_row = []  # Initialize an empty list for each row
            for x, piece in enumerate(row):
                piece_color = COLOR_MAPS[piece[0]]
                piece_name = PIECE_MAPS[piece[1]]
                if piece_name in PIECES_THAT_REQUIRE_BOARD_INFO:
                    if piece_name == "wizard":
                        movememnts_class = wizard
                    # remember to add it to the import statement at the top
                    # elif piece_name == "...":
                    #     movememnts_class = ...
                    else:
                        raise TypeError("type 'requires' the board information, but isn't defined in the ChessBoard __init__ class")
                    # movements_class exists, and now it's time to fuck shit up
                    my_moves = PieceMovements(piece_name)
                    if "see hidden" in movememnts_class:
                        # get rid of "see hidden"
                        movememnts_class.remove_particular_move("see hidden")
                        for x in game_template:
                            for y in x:
                                if y == HIDDEN_ID:
                                    my_moves.add((x, y))
                    if "see empty" in movememnts_class:
                        # get rid of "see empty"
                        movememnts_class.remove_particular_move("see empty")
                        for x in game_template:
                            for y in x:
                                if y == EMPTY_ID:
                                    my_moves.add((x, y))
                    new_piece = Piece(name=piece_name, color=piece_color, piece_id=generate_piece_id(piece_name, x, y), move=my_moves)
                else:
                    new_piece = Piece(name=piece_name, color=piece_color, piece_id=generate_piece_id(piece_name, x, y))
                board_row.append(new_piece)
            self.board.append(board_row)

    def __repr__(self):
        result = ""
        for y, row in enumerate(self.board):
            for x, piece in enumerate(row):
                result += f"({x}, {y}, {piece.name}) "
            result += "\n"
        return result

    def __str__(self):
        result = ""
        for y, row in enumerate(self.board):
            for x, piece in enumerate(row):
                if piece.name != "hidden":
                    result += f"{piece.name:^8}|"
            result += "\n"
        return result


class Piece:
    # from piece_setups import pawn, knight, rook, bishop, queen, king
    def __init__(self, name: str, color, piece_id, move: PieceMovements = None):
        self.color = color  # : "white" or "black" usually...
        self.moves_made = 0
        self.id = piece_id
        self.name = name  # pawn, knight, rook, bishop, queen, king
        if not move:
            if name in NON_MOVABLE_PIECE_TYPES:
                self.move = PieceMovements("empty")  # sets up empty movements class
            elif name == "pawn":
                self.move = pawn  # default vals in ./piece_setups.py
            elif name == "knight":
                self.move = knight
            elif name == "rook":
                self.move = rook
            elif name == "bishop":
                self.move = bishop
            elif name == "queen":
                self.move = queen
            elif name == "king":
                self.move = king
        else:
            self.move = move

    def __repr__(self):
        return f"{self.color} {self.name}"

    def replace_old_position_with_empty(self, board, from_x, from_y):
        # if piece is a wizard, maybe make the old position a hidden one to funk it up?
        board[from_x][from_y] = Piece("empty", "empty", generate_piece_id("empty", from_x, from_y))

    def move_new_piece_to_position(self, board, to_x, to_y):
        piece_to_be_taken = board[to_x][to_y]
        # if piece is not nothing (enemy piece was taken)
        if piece_to_be_taken.name not in NON_MOVABLE_PIECE_TYPES:
            # in form (color, name)
            taken_pieces.append(piece_to_be_taken.color, piece_to_be_taken.name)

        board[to_x][to_y] = self  # sets it to its own piece class

    # def get_board_h_and_w(self, board):
    #     # gets the board max height and max width
    #     len_board_width = len(board)
    #     if SQUARE_BOARD:
    #         len_board_height = len(board[0])
    #     else:
    #         len_board_height = max([len(board[k]) for k in range(len(board))])
    #         # assuming non-square board
    #
    #     return len_board_width, len_board_height

    def move_to(self, board, friendly_pieces_color, from_x, from_y, to_x, to_y):
        # check spot is a valid move
        if (to_x, to_y) in self.get_moves(board, self.color, from_x, from_y):
            # spot exists so you can move there, replace your position with an empty, add piece to the taken pieces
            # move new piece to position
            self.move_new_piece_to_position(board, to_x, to_y)
            # replace old with empty
            self.replace_old_position_with_empty(board, from_x, from_y)
        else:
            print("spot already has a piece, try again")

    def get_moves(self, board: list[list[any]], friendly_pieces_color: str or set[str], from_x, from_y):
        # ignoring other pieces and collisions
        moves = set()  # set to force it as no duplicates
        if isinstance(friendly_pieces_color, str):
            from_piece_color = set(friendly_pieces_color)
        elif not isinstance(friendly_pieces_color, set):
            raise TypeError("friendly_pieces_color not a string or a set of strings", friendly_pieces_color)

        friendly_pieces_color.add("--")  # only happens assuming friendly_pieces_color is a set

        # lambda func, does as it says.
        # assumes board is full of 'Pieces' custom objects, INCLUDING EMPTY SLOTS
        def is_touching_enemy(x_pos, y_pos) -> bool:
            if len(board) < x_pos:
                return False  # board doesn't go that far, we would get an index error
            if len(board[x_pos] < y_pos):
                return False  # board doesn't go that far
            if isinstance(board[x_pos][y_pos], Piece):
                return not board[x_pos][y_pos].color in from_piece_color
            else:
                raise TypeError("☹️ some unidentified piece has entered the game-board, good luck\n\nboard: ↓\n", board)

        # first move (pawns move 2)
        if self.moves_made == 0:
            # could be type == "f"
            if self.move.has_loc_of_type("f"):
                first_moves = self.move.get_loc_of_type("f")
                k = 0
                while (k < first_moves) and (
                not is_touching_enemy(from_x[0] + first_moves[k][0], from_y[1] + first_moves[k][1])):
                    # adds the (current x + the rel x), (current y + the rel y)
                    moves.add((from_x[0] + first_moves[k][0], from_y[1] + first_moves[k][1]))
                    k += 1
        # castle + queen move left right up down
        if self.move.has_loc_of_type("a"):
            # absolute( horizontal / vertical )
            abs_moves = self.move.get_loc_of_type("a")

            # note on non-square boards ie (triangle boards),
            # the code assumes the worst position possible

            # horizontal
            if abs_moves[0] is True:
                # left
                current_x = from_x - 1
                while not is_touching_enemy(current_x, from_y):
                    moves.add((current_x, from_y))
                    current_x -= 1

                # right
                current_x = from_x + 1
                while not is_touching_enemy(current_x, from_y):
                    moves.add((current_x, from_y))
                    current_x += 1

            # vertical
            if abs_moves[1] is True:
                # down
                current_y = from_y - 1
                while not is_touching_enemy(from_x, current_y):
                    moves.add((from_x, current_y))
                    current_y -= 1

                # up
                current_y = from_y + 1
                while not is_touching_enemy(from_x, current_y):
                    moves.add((from_x, current_y))
                    current_y += 1

        # diagonals / bishop + queen
        if self.move.has_loc_of_type("d"):
            # diagonal
            diagonal_moves = self.move.get_loc_of_type("d")
            for diagonal_move in diagonal_moves:
                # bottom left to top right
                if diagonal_move[0]:
                    # to bottom left
                    current_x = from_x - 1
                    current_y = from_y - 1
                    while not is_touching_enemy(current_x, current_y):
                        moves.add((current_x, current_y))
                        current_x -= 1
                        current_y -= 1
                    # to top right
                    current_x = from_x + 1
                    current_y = from_y + 1
                    while not is_touching_enemy(current_x, current_y):
                        moves.add((current_x, current_y))
                        current_x += 1
                        current_y += 1
                # bottom right to top left
                if diagonal_move[0]:
                    # to bottom right
                    current_x = from_x + 1
                    current_y = from_y - 1
                    while not is_touching_enemy(current_x, current_y):
                        moves.add((current_x, current_y))
                        current_x += 1
                        current_y -= 1
                    # to top left
                    current_x = from_x - 1
                    current_y = from_y + 1
                    while not is_touching_enemy(current_x, current_y):
                        moves.add((current_x, current_y))
                        current_x -= 1
                        current_y += 1

        if self.move.has_loc_of_type("e"):
            # only able to move if there is an enemy, pawns
            # can move diagonal & forwards only when taking pieces
            # color: "black" or "white"
            movements_only_enemies = self.move.get_loc_of_type("e")
            for only_enemy_x, only_enemy_y in movements_only_enemies:
                new_x, new_y = ((only_enemy_x + from_x), (only_enemy_y + from_x))
                if board[new_x][new_y]:
                    # piece is there, check it is not a friendly piece
                    if is_touching_enemy(new_x, new_y):
                        # if it is an enemy, then add it to the possible moves
                        moves.add((new_x, new_y))

        if self.move.has_loc_of_type("s"):
            # basically king checks every god dam piece to make sure it won't die...

            def not_an_empty_piece(my_piece):
                if isinstance(my_piece, Piece):
                    return my_piece.name != "empty"
                raise TypeError("piece not right")

            def relevant_pieces_to(my_x, my_y, my_board):
                # OPTIMISE,
                # use backtracking to check if a piece is blocking a path,
                # therefore invalidating ones behind, also check no horse archetypes
                result = []
                for x in my_board:
                    for y, baddie_piece in enumerate(x):
                        result.append(baddie_piece)
                return result

            def is_dangerous_piece(my_x, my_y, piece):
                if (my_x, my_y) in piece.get_moves(board, piece.color, piece.id, piece.move):
                    return True
                return False

            # must check every god dam piece
            baddie_pieces = relevant_pieces_to(from_x, from_y, board)
            for baddie in baddie_pieces:
                if not_an_empty_piece(baddie):  # not an empty spot
                    if not is_dangerous_piece(from_x, from_y, baddie):
                        moves.add((from_x, from_y))
        return moves





if __name__ == "__main__":
    print(start_game())
