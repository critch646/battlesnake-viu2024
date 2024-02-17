from RandomPlayer import RANPlayer
from HumanPlayer import HumanPlayer
from AgentPlayer import AgentPlayer
from Board import Rows, Columns, Players, playerMarble, Goal, Status
from Board import displayBoard, checkWinner, checkDraw
from copy import deepcopy

# Constants
Filling = ' '

# Function to initialize the game board and column tops
def initBoard():
    board = [[Filling for _ in range(Columns)] for _ in range(Rows)]
    top = [0 for _ in range(Columns)]
    return board, top

# Main game loop
def main():
    board, top = initBoard()
    player = Players - 1  # initialize the last player (so that the game starts with player 0)
    p = [None, None]

    p[0] = RANPlayer(Rows, Columns, Goal)  # HumanPlayer(playerMarble[0]) is also avaiable here
    p[1] = AgentPlayer(playerMarble[1], "B", 3)

    status = Status.Continue
    position = -1

    print("\n=== Connect Four ===\n")

    while status == Status.Continue:
        displayBoard(board)
        # Switch between players
        player = (player + 1) % Players
        position = p[player].move(deepcopy(board), deepcopy(top))

        # Validate move
        while position < 0 or position >= Columns or top[position] >= Rows:
            print("Invalid move! Please choose a column that's not full.")
            print(p[player].getName(), "tried to go in column:", position+1)
            position = p[player].move(deepcopy(board), top)

        # Check for cheating
        if position < 0 or position >= Columns or top[position] >= Rows:
            print(f"Player {p[player].getName()} is cheating!")
            status = Status.Cheating
            continue

        # Make the move
        board[top[position]][position] = playerMarble[player]
        top[position] += 1

        # Check for winner
        status = checkWinner(board, player)
        if status != Status.Win:
            # If no winner, check for draw
            status = checkDraw(top, Columns, Rows)

    # Game over, display final state and outcome
    displayBoard(board)

    if status == Status.Cheating:
        print(f"Player {p[player].getName()} is cheating!")
    elif status == Status.Draw:
        print("\n  *** It is a draw! ***\n")
    else:
        print(f"\n  *** Congratulations! Player {p[player].getName()} ***")
        print("  *** You won the game. ***\n")

# main function to start game
if __name__ == "__main__":
    main()
