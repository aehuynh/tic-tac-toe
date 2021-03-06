from copy import deepcopy
import random

class Board(object):
    """A model representing a Tic-Tac-Toe game board."""

    NUM_ROWS = 3
    NUM_COLS = 3
    DRAW = "DRAW"

    def __init__(self):
        # Create a 3x3 2d array to represent the board in (row, col) format
        self.cells = [[None for x in range(self.NUM_COLS)] for y in range(self.NUM_ROWS)]
        # List of 3 cells that represent a winning combination     
        self.winning_combos = self.generate_winning_combos()
    
    def generate_winning_combos(self):
        """Generate all winning combinations of cells.

        Returns a list of lists of tuples.

        Each tuple represents one cell.
        Each inner list represents one winning combination, consisting of 3 cells.
        If a player has marked all 3 cells in one winning combination, he/she has won.
        """
        winning_combos = []
        # Add win by row combos
        for row in range(self.NUM_ROWS):
            winning_combo = []
            for col in range(self.NUM_COLS):
                winning_combo.append((row, col))
            winning_combos.append(winning_combo)

        # Add win by column combos
        for col in range(self.NUM_COLS):
            winning_combo = []
            for row in range(self.NUM_ROWS):
                winning_combo.append((row, col))
            winning_combos.append(winning_combo)

        # Add win by diagonal combos 
        winning_combos.append([(0,2), (1,1), (2,0)])
        winning_combos.append([(0,0), (1,1), (2,2)])
        
        return winning_combos

    def available_moves(self):
        """Returns all available moves on the board right now."""
        moves = []
        for row in range(self.NUM_ROWS):
            for col in range(self.NUM_COLS):
                if self.cells[row][col] is None:
                    moves.append((row,col))
        return moves

    def make_move(self, move, mark):
        """Add mark to the cell indicated by the parameter move"""
        row = move[0]
        col = move[1]
        # if row or col is not in range of board
        if row not in range(self.NUM_ROWS) or col not in range(self.NUM_COLS):
            return None

        if self.cells[row][col] is None:
            self.cells[row][col] = mark
            return True
        # else the cell is already marked

    def check_win_or_draw(self):
        """Check if the board is at end game state.

        Returns the mark of the winner if one is found or self.DRAW if there
        is a draw.
        """
        # Check board for winning combos
        for winning_combo in self.winning_combos:
            pos1, pos2, pos3 = winning_combo[0], winning_combo[1], winning_combo[2]
            mark = self.cells[pos1[0]][pos1[1]]
            if mark is not None:
                if mark == self.cells[pos2[0]][pos2[1]] == self.cells[pos3[0]][pos3[1]]:
                    return mark

        # If every cell has been marked and no one has won
        if len(self.available_moves())== 0:
            return Board.DRAW

    def display(self):
        """Prints the current state of the Tic-Tac-Toe board."""
        for row in range(self.NUM_ROWS):
            row_display = ""
            for col in range(self.NUM_COLS):
                row_display += self.cells_to_str(row, col)
                # Add separation between columns
                if col != self.NUM_COLS-1:
                    row_display += " | "
            print(row_display)

            # Add separation between rows
            if row != self.NUM_ROWS-1:
                print("---------------")

    def cells_to_str(self, row, col):
        """Returns a string form of a cell to be viewed by the user."""
        mark = self.cells[row][col]
        if mark:
            return " " + mark + " "
        else:
            return str(row) + "," + str(col)

    def clone(self):
        """Creates a clone of this board."""
        b = Board()
        # Deep copy list because a simple copy still copies references 
        # to the inner lists instead of creating new inner lists 
        b.cells = deepcopy(self.cells)
        return b
        # TODO: consider refactoring to not use a clone method


class Player(object):
    """A model representing a Tic-Tac-Toe player."""

    def __init__(self, mark="X"):
        self.wins = 0
        self.draws = 0
        self.losses = 0
        self.mark = mark

    def win(self):
        self.wins += 1

    def lose(self):
        self.losses += 1

    def draw(self):
        self.draws += 1 

class Bot(Player):
    """A model that repesents a Bot that plays Tic-Tac-Toe. 

    The bot is capable of figuring out moves on its own.
    """
    # Bot difficulty modes
    EASY_MODE = 0
    NORMAL_MODE = 1
    IMPOSSIBLE_MODE = 2
    AVAIBLE_MODES = (EASY_MODE, NORMAL_MODE, IMPOSSIBLE_MODE)

    def __init__(self, mark="X", mode=EASY_MODE):
        super().__init__(mark)
        self.mode = mode

    def opponent_mark(self):
        """Get the mark of the opponent."""
        if self.mark == "X":
            return "O"
        else:
            return "X"

    def next_move(self, board):
        """Returns the next move that this bot will make.

        Chooses which move to generate based on difficulty set at the beginning
        of the game.
        """
        if self.mode is Bot.EASY_MODE:
            return self.easy_move(board)
        elif self.mode is Bot.NORMAL_MODE:
            return self.normal_move(board)
        else:
            return self.impossible_move(board)

    def easy_move(self, board):
        """Choose a random move out of all available moves."""
        return random.choice(board.available_moves())

    def normal_move(self, board):
        """Choose a semi-smart move. 

        It chooses from three types of moves(in order of priority):
        1. Any move that will allow the bot to win
        2. Any move that will block the opponent from winning in the 
           next turn
        3. A random move
        """
        # Choose any move that would allow bot to win
        for move in board.available_moves():
            # Make this move for bot and see what happens
            bot_next = board.clone()
            bot_next.make_move(move, self.mark)
           
            # If bot will win, choose the move to win
            if bot_next.check_win_or_draw():
                return move

        # Check for moves to block an opponent from winning
        for move in board.available_moves():
            # The reason for separating this from the loop above is to
            # make sure the bot chooses any winning moves before blocking moves
            opponent_next = board.clone()
            opponent_next.make_move(move, self.opponent_mark())

            if opponent_next.check_win_or_draw():
                return move

        # Otherwise choose a random move
        return self.easy_move(board)

    def impossible_move(self, board):
        """The "Perfect" move that will end with the bot either winning 
        or getting a draw.

        The impossible move leverages the minimax algorithm to figure out all
        possible outcomes(other than insignificant outcomes) and picks the best one.
        """

        # On the first move, randomly choose either the center or a corner.
        # Both of these moves lead to an optimal outcome. This improves 
        # evaluation time by a factor of 9 without affecting the win rate.
        if len(board.available_moves()) == Board.NUM_COLS * Board.NUM_ROWS:
            if bool(random.getrandbits(1)):
                # Return center
                return (1,1)
            else:
                # Return a random corner
                corners = [(0,0), (2,0), (0,2), (2,2)]
                return random.choice(corners)
     
        move, result = self.minimax(board, self.mark)

        return move

    def minimax(self, board, current_mark):
        """Minimax algorithm applied to Tic Tac Toe.

        No optimizations are needed because the number of available outcomes is
        at most 8*7*6*5*4*3*2*1 = 40320. Hard coding the first move sped up
        the algorithm fast enough to work well.

        Returns the move chosen and the value of this node in the form: move, result 
        """
        moves = board.available_moves()

        # Return heuristic value of node if there is a win or draw
        mark = board.check_win_or_draw()
        if mark:
            if mark is self.mark:
                return None, 10
            elif mark is self.opponent_mark():
                return None, -10
            return None, 0

        # Set data on whether to maximize or minimize 
        if current_mark is self.mark:
            best_result = -10000000000000
            next_mark = self.opponent_mark()
        else:
            best_result = 10000000000000000
            next_mark = self.mark

        best_move = None
        for move in moves:
            # Simulate the move and see the result 
            b = board.clone()
            b.make_move(move, current_mark)
            next_move, result = self.minimax(b, next_mark)

            # Check if this move is the best move
            if current_mark is self.mark:
                if result > best_result:
                    # Decrement result to make immediate winning moves 
                    # more valuable to bot
                    result -= 1

                    best_result = result
                    best_move = move
            if current_mark is self.opponent_mark():
                if result < best_result:
                    # Increment result to make immediate wnning moves 
                    # more valuable to opponent
                    result += 1
                    
                    best_result = result
                    best_move = move

        return best_move, best_result