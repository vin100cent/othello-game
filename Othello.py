# Author: Vincewa Tran
# GitHub Username: vin100cent
# Date: 06/30/23
# Description: This program represents a 2d console version of the Othello
# board game. There are two classes a Player class and Othello class. The
# Othello class contains the bulk of methods for playing the game. Outside of
# both classes are decorators and a tuple of coordinate directions around a
# game piece in Othello
from functools import wraps

# gloabl variables for the three different values a coordinate on the board
# can have
BLACK = 'X'
EMPTY = '.'
WHITE = 'O'

# a list of tuples containing directions that a piece can go
MOVE_DIR = \
    [(-1, -1), (-1, 0), (-1, +1),
     (0, -1),            (0, +1),
     (+1, -1), (+1, 0), (+1, +1)]

def board_decorator(func):
    """
    Decorates the board with score, edge elemeents and valid moves
    """
    @wraps(func)
    def wrapper(self):
        b_score, w_score = self.get_score('black'), self.get_score('white')
        print(f"Black:{b_score} | White:{w_score}")
        print('@ y 1 2 3 4 5 6 7 8 @ ')
        print('x * * * * * * * * * * ')
        func(self)
        print('@ * * * * * * * * * * ')
        print(f"Black Moves: {self.return_available_positions('black')}")
        print(f"White Moves: {self.return_available_positions('white')}")
    return wrapper


class Player:
    """
    Player object with name and color as attributes
    """

    def __init__(self, name, color):
        self.name = name
        self.color = color
        self.score = 2
        self.valid_moves = []

class Othello:
    """
    initializes a board with pieces randomized while keeping within
    othello's rules. contains a method to print board, create players,
    get score, determine winner, find available positions, make moves,
    flip pieces after a move, and a play method
    """

    def __init__(self):
        self._board = [["." for _ in range(10)] for _ in range(10)]
        self._board[4][4] = WHITE
        self._board[4][5] = BLACK
        self._board[5][4] = BLACK
        self._board[5][5] = WHITE
        self._players = {}

    @board_decorator
    def print_board(self):
        """
        Prints the board
        """
        for x in range(8):
            print(x + 1, end=" * ")
            for y in range(8):
                print(self._board[y + 1][x + 1], end=" ")
            print("*")

    def create_player(self, name, color):
        """
        Creates a player and adds it to the players dictionary
        """
        player = Player(name, color)
        self._players[color] = player

    def get_piece(self, color):
        if color == 'black':
            return BLACK
        else:
            return WHITE

    def get_op(self, color):
        if color == 'black':
            return 'white'
        else:
            return 'black'

    def get_color_from_coord(self, piece_position):
        """
        Returns a string color for a coordinate
        """
        col, row = piece_position
        if self._board[row][col] == BLACK:
            return 'black'
        else:
            return 'white'

    def get_score(self, color):
        """
        Returns the score for a specified color piece
        """
        piece = self.get_piece(color)
        score = 0
        for x in range(8):
            for y in range(8):
                if self._board[y + 1][x + 1] == piece:
                    score +=1
        return score

    def update_players(self):
        """
        updates the values inside of the player class
        """
        for color in self._players:
            self._players[color].score = self.get_score(color)
            self._players[color].valid_moves = \
                self.return_available_positions(color)

    def is_empty(self, coord):
        """
        Checks if a coordinate is an empty space or note and returns a
        boolean value
        """
        column, row = coord
        if self._board[row][column] == EMPTY:
            return True
        return False

    def is_board_full(self):
        """
        Returns a boolean value for whether or not the board is full
        """
        open_spaces = 0
        for x in range(8):
            for y in range(8):
                if self._board[y + 1][x + 1] == EMPTY:
                    open_spaces += 1
        return open_spaces == 0

    def get_2d_board(self):
        """
        Returns a 2d array representation of the current board
        """
        matrix = [['*'] * 10 for _ in range(10)]
        for row in range(1, 9):
            for col in range(1, 9):
                matrix[col][row] = self._board[row][col] #matrix = board reverse
        return matrix

    def return_winner(self):
        """
        Returns the winner in the format "Winner is 'color' player: 'name"
        """
        if self._players['black'].score == self._players['white'].score:
            return "It's a tie"
        if self._players['black'].score > self._players['white'].score:
            return f"Winner is black player: {self._players['black'].name}"
        return f"Winner is white player: {self._players['white'].name}"

    def return_available_positions(self, color):
        """
        Returns available positions for a specified color as a list
        """
        positions = []
        for col in range(1, 9):
            for row in range(1, 9):
                if self._board[row][col] == EMPTY and self.is_valid(color, \
                        row, col):
                        positions.append((col, row))
        return positions

    def is_valid_coord(self, row, col):
        """
        Used by other methods to keep moves in bounds of the othello board
        """
        return 0 < row < 9 and 0 < col < 9

    def is_valid(self, color, row, col):
        """
        Returns a boolean value for whether or not a coordinate is a valid
        play for a given color
        """
        if self._board[row][col] != EMPTY:
            return False
        for dir in MOVE_DIR:
            if self.validate_dir(row, col, dir[0], dir[1], color):
                return True
        return False

    def validate_dir(self, row, col, dx, dy, color, count=0):
        """
        Recursively searches down each direction to check if a given
        direction is valid. A valid direction has the start/end nodes as the
        passed in color with pieces of the opposing color sandwiched between.
        """
        new_row = row + dx
        new_col = col + dy
        if not self.is_valid_coord(new_row, new_col):
            return False
        if self._board[new_row][new_col] == self.get_piece(color):
            return count > 0
        if self._board[new_row][new_col] == EMPTY:
            return False
        return self.validate_dir(new_row, new_col, dx, dy, color, count + 1)

    def flip_pieces(self, piece_position):
        """
        Flips over pieces after a move. This function makes use of the
        validate_dir to check if there are pieces to flip and adds found
        pieces to a list. The items within the list are finally flipped to
        the correct color.
        """
        col, row = piece_position
        player_piece = self._board[row][col]
        color = self.get_color_from_coord(piece_position)
        pieces_to_flip = []
        for dir in MOVE_DIR:
            dx, dy = dir
            count = 1
            new_row = row + (dx * count)
            new_col = col + (dy * count)
            while self.validate_dir(row, col, dx, dy, color) and self._board[
                new_row][new_col] != player_piece:
                pieces_to_flip.append([new_col, new_row])
                count += 1
                new_row = row + (dx * count)  # Update new_row within the loop
                new_col = col + (dy * count)  # Update new_col within the loop
        for coord in pieces_to_flip:
            flip_col, flip_row = coord
            self._board[flip_row][flip_col] = player_piece

    def make_move(self, color, piece_position):
        """
        Places a specified color piece on the board at a coordinate
        Return board as a 2d list
        """
        column, row = piece_position
        self._board[row][column] = self.get_piece(color)
        self.flip_pieces(piece_position)
        self.return_available_positions(color)
        self.update_players()
        return self.get_2d_board()

    def play_game(self, color, piece_position):
        """
        Plays the game by assessing the validity of a move and whether the
        game has ended or note. If end conditions are met play_game returns
        the winner. If an invalid move is entered the valid moves for the
        passed in color is returned.
        """
        if len(self.return_available_positions(color)) == 0  and len(
                self.return_available_positions(self.get_op(color))) == 0:
            print(self.return_winner())
        if len(self.return_available_positions(color)) == 0 and len(
                self.return_available_positions(self.get_op(color))) > 0:
            print ('Pass Turn')
        if piece_position in self.return_available_positions(color):
            self.make_move(color, piece_position)
            self.print_board()
            if self.is_board_full() == True:
                print(self.return_winner())
        else:
            print(f'Here are the valid moves:'
                  f'{self.return_available_positions(color)}')
            return 'Invalid move'

if __name__ == "__main__":
    game = Othello()
    game.create_player("Helen", "white")
    game.create_player("Leo", "black")
    game.print_board()
    game.play_game('black', (4, 3))
    game.play_game('white', (5, 3))
    game.play_game('black', (6, 6))
    game.play_game('white', (3, 2))
    game.play_game('black', (5, 2))
    game.play_game('white', (6, 3))
    game.play_game('black', (2, 1))
    game.play_game('white', (3, 6))
    game.play_game('black', (4, 6))
    game.play_game('white', (5, 6))
    game.play_game('black', (5, 7))
    game.play_game('white', (4, 2))
    game.play_game('black', (3, 5))
    game.play_game('white', (4, 7))
    game.play_game('black', (2, 7))
    game.play_game('white', (1, 8))
    game.play_game('black', (2, 6))
    game.play_game('white', (1, 7))
    game.play_game('black', (1, 6))
    game.play_game('white', (1, 5))
    game.play_game('black', (2, 8))
    game.play_game('white', (3, 8))
    game.play_game('black', (2, 4))
    game.play_game('white', (3, 3))
    game.play_game('black', (3, 1))
    game.play_game('white', (4, 1))
    game.play_game('black', (3, 7))
    game.play_game('white', (1, 1))
    game.play_game('black', (5, 1))
    game.play_game('white', (7, 7))
    game.play_game('black', (3, 4))
    game.play_game('white', (2, 5))
    game.play_game('black', (1, 3))
    game.play_game('white', (4, 8))
    game.play_game('black', (7, 2))
    game.play_game('white', (2, 3))
    game.play_game('black', (5, 8))
    game.play_game('white', (6, 1))
    game.play_game('black', (1, 4))
    game.play_game('white', (6, 5))
    game.play_game('black', (6, 7))
    game.play_game('white', (2, 2))
    game.play_game('black', (1, 2))
    game.play_game('white', (8, 1))
    game.play_game('black', (6, 2))
    game.play_game('white', (6, 4))
    game.play_game('black', (7, 3))
    game.play_game('white', (6, 8))
    game.play_game('black', (7, 1))
    game.play_game('white', (7, 4))
    game.play_game('black', (7, 5))
    game.play_game('white', (8, 3))
    game.play_game('black', (8, 4))
    game.play_game('white', (7, 6))
    game.play_game('black', (7, 8))
    game.play_game('white', (8, 2))
    game.play_game('white', (8, 6))
    game.play_game('black', (8, 5))
    game.play_game('white', (8, 7))
    game.play_game('white', (8, 8))


























