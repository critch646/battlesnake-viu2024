import random
import time

class RANPlayer:

    # Static variable to generate unique names for players
    num = ord('A')

    # Constructor initializes a new random player with given board parameters and goal
    def __init__(self, r=6, c=7, g=4):
        self.Rows = r
        self.Columns = c
        self.Goal = g

        self.name = "Random_Player_" + chr(RANPlayer.num)
        RANPlayer.num += 1   # Increment the character for next player name

        # Seed the random number generator with current time
        random.seed(time.time())

    # Method to make a move on the board (chosen randomly)
    def move(self, board, top):

        # Calculate the number of valid columns where a marble can be placed
        count = sum(1 for i in range(self.Columns) if top[i] < self.Rows)

        assert count > 0
        # Select a random index for a move
        index = random.randint(0, count - 1)

        # Loop through the columns to find a valid column for the selected index
        for col in range(self.Columns):
            if top[col] < self.Rows:
                index -= 1
            if index < 0:
                return col

    def getName(self):
        return self.name
