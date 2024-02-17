class HumanPlayer:
    def __init__(self, name="Human"):
        self.name = name

    def move(self, board, top):
        while True:
            try:
                col = int(input("Enter your move (1-7): ")) - 1
                if 0 <= col < 7:
                    return col
                else:
                    print("Invalid move! Please choose a column between 1 and 7.")
            except ValueError:
                print("Invalid input! Please enter a number between 1 and 7.")
    
    def getName(self):
        return self.name
