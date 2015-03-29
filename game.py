import random
from models import Player, Board, Bot

class Game(object):

    def __init__(self):
        self.bot = Bot()
        self.human = Player()

    def start(self):
        """Controls the flow of the entire game."""
        while(True):
            self.board = Board()
            self.display_intro()
            self.decide_mode()
            self.assign_marks()
            result = self.play_game()
            self.update_scoreboard(result)
            self.display_scoreboard()

            if self.play_again() is None:
                print("\nHave a good day!")
                break

    def display_intro(self):
        print("Welcome. This is a text based game of Tic-Tac-Toe against a smart bot. ")
        print("You will be given a number of options to choose from. Please enter only integers. ")

    def decide_mode(self):
        """Prompt user for bot difficulty and set bot to that difficulty."""
        print("There are 3 modes: easy, medium and impossible. \n")
        print("Easy mode: " + str(Bot.EASY_MODE))
        print("Normal mode: " + str(Bot.NORMAL_MODE))
        print("Impossible mode: " + str(Bot.IMPOSSIBLE_MODE) + "\n")

        mode = None
        while mode not in Bot.AVAIBLE_MODES:
            mode = self.input_int("Please choose a mode: ")
            if mode not in Bot.AVAIBLE_MODES:
                print("The input was invalid. Please try again. ")  

        self.bot.mode = mode

    def assign_marks(self):
        """Randomly assign 'X' or 'O' to the human player and bot. The 
        player with the 'X' mark goes first.
        """
        if bool(random.getrandbits(1)):
            self.bot.mark = "X"
            self.human.mark = "O"
            print("You are O and will be going second. \n")
        else:
            self.bot.mark = "O"
            self.human.mark = "X"
            print("You are X and will be going first. \n")

    def play_game(self):
        """Start requesting and making moves on game board. """
        # If bot goes first
        if self.bot.mark is "X":
            self.board.make_move(self.bot.next_move(self.board), self.bot.mark)

        human_turn = True
        while(len(self.board.available_moves())):
            if human_turn:
                self.board.make_move(self.ask_human_for_move(), self.human.mark)
            else:
                self.board.make_move(self.bot.next_move(self.board), self.bot.mark)

            result = self.board.check_win_or_draw()
            if result:
                self.board.display()
                return result

            human_turn = not(human_turn)

        return Board.DRAW

    def ask_human_for_move(self):
        """ Prompt user for a move. 

        Returns a tuple containing the move that the user chose.
        """
        self.board.display()
        print("\nIt is your turn!\n")

        available_moves = self.board.available_moves()

        # Show all possible moves and the number to make the moves
        for index, value in enumerate(available_moves):
            print("%s: "% (value,) + str(index))
        print("")

        # Ask for a move and parse the input
        choice = -1
        while choice not in range(len(available_moves)):
            choice = self.input_int("You are %s.\n\nPlease choose your next move: " % (self.human.mark))
            if choice not in range(len(available_moves)):
                print("The input was invalid. Please try again. ")
        print("")
        return available_moves[choice]

    def update_scoreboard(self, result):
        """Update wins, losses and/or draws."""
        if result is Board.DRAW:
            self.bot.draw()
            self.human.draw()
            print("\nDRAW! No one wins. ")
        elif result is self.bot.mark:
            self.bot.win()
            self.human.lose()
            print("\nThe Bot wins! ")
        else:
            self.bot.lose()
            self.human.win()
            print("\nYou win!")
    
    def display_scoreboard(self):
        print("\nScoreboard:")
        print("\nBot wins: " + str(self.bot.wins))
        print("Your wins: " + str(self.human.wins))
        print("Draws: " + str(self.human.draws))
    
    def input_int(self, prompt):
        """Keep requesting for input until a valid integer is entered.

        Returns an integer
        """
        choice = -1
        while(choice == -1):
            try:
                choice = input(prompt).strip()
                choice = int(choice)
            except ValueError:
                choice = -1
                print("You did not enter an integer. Please try again. ")

        return choice

    def play_again(self):
        """Ask the user if he or she wants to play again.

        Returns True if user wants to play again.
        """
        choice = input("\nIf you would like to play again, please type \"yes\": ").strip()
        if "yes" in choice.lower():
            print("\n")
            return True
    

if __name__ == "__main__":
    tic_tac_toe = Game()
    tic_tac_toe.start()
   
