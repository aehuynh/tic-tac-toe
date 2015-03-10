# Tic Tac Toe
A text-based Tic Tac Toe game with an unbeatable bot 

### Table of Contents

1. [Motivations](#motivations)

2. [How to Player](#how)

3. [Game Modes](#modes)

4. [Algorithm Used for Impossible Mode](#algorithm)

<a name="motivations" \>
###  Motivations
I was taking the free online <a href="http://ocw.mit.edu/courses/electrical-engineering-and-computer-science/6-034-artificial-intelligence-fall-2010/index.htm">Artificial Intelligence course</a> by MIT
and wanted to create a simple AI bot. Tic tac toe seemed like the easiest game to create an AI bot for since
it only has at most 9! = 362880 different variations of the board.

<a name="how" \>
###  How to Play
The only dependency is Python3. The game will start on the command: `python game.py`

<a name="modes" \>
###  Game Modes
There are 3 game modes:

1. **Easy**:       The bot chooses random moves.
2. **Normal**:     The bot forecasts 1 move ahead and chooses winning moves and/or blocks losing moves.
3. **Impossible**: The bot cannot lose. It decides on a move after creating all variations of moves all the way to 
               the end of the game.

<a name="algorithm" \>
###  Algorithm Used for Impossible Mode
The impossible mode bot uses the **minimax algorithm** to forecast all possible outcomes and chooses a move
that will always lead to either a draw or a win.

**There are slight variations to the minimax algorithm:**

1. Wins that take less moves are ranked higher
2. If the bot goes first, it will randomly pick either a corner or the center instead of forecasting
   a move.

\#2 speeds up the wait time by a factor of 9 without affecting performance at all. 

There weren't any other optimizations to the minimax algorithm needed (like alpha-beta pruning). The 
number of possible outcomes is small enough that performance is not an issue. 

