# Required Imports
from enum import Enum

# Constants
Columns = 7
Rows = 6
Goal = 4
Players = 2
playerMarble = ['X', 'O']

# Check for draw condition (all columns are full)
def checkDraw(top, Columns, Rows):
    for i in range(Columns):
        if top[i] < Rows:
            return Status.Continue
    return Status.Draw

class Status(Enum):
    Win = 1
    Draw = 2
    Continue = 3
    Cheating = 4

# Check all directions for winning conditions for a player
def checkWinner(board, player):
    rows, cols = len(board), len(board[0])
    
    # Vertical check
    for col in range(cols):
        if checkLine(board, 0, col, 1, 0, player) == Status.Win:
            return Status.Win
    
    # Horizontal check
    for row in range(rows):
        if checkLine(board, row, 0, 0, 1, player) == Status.Win:
            return Status.Win
    
    # Diagonal checks (bottom left to top right and top left to bottom right)
    for row in range(rows):
        for col in range(cols):
            if checkLine(board, row, col, 1, 1, player) == Status.Win:
                return Status.Win
            if checkLine(board, row, col, -1, 1, player) == Status.Win:
                return Status.Win
    
    return Status.Continue

# Check for winning line starting from (row, col) with given direction (rdelta, cdelta)
def checkLine(board, row, col, rdelta, cdelta, player):
    count = 0
    rows, cols = len(board), len(board[0])
    
    while 0 <= row < rows and 0 <= col < cols:
        if board[row][col] == playerMarble[player]:
            count += 1
            if count == Goal:
                return Status.Win
        else:
            count = 0
        row += rdelta
        col += cdelta
    
    return Status.Continue

# Function to display the game board
def displayBoard(board):
    print()
    for i in range(len(board) - 1, -1, -1):
        print("-" + "----" * len(board[i]))
        print("|", end="")
        for j in board[i]:
            print(f" {j} |", end="")
        print()
    print("-" + "----" * len(board[0]))
    for j in range(1, len(board[0]) + 1):
        print(f"  {j}", end=" ")
    print("\n")