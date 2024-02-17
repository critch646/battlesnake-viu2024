class State:

    def __init__(self, board):
        # reference to the current state of the game board
        self.snakes = [Snake(snake) for snake in board["snakes"]]
        self.snakes.append(Snake(board["you"]))
        self.height = board["height"]
        self.width = board["height"]

        pass


class Snake:
    def __init__(self, snake):
        self.name = snake["name"]
        self.health = snake["health"]
        self.body = snake["body"]
        self.head = snake["head"]
        self.length = snake["length"]


class AdversarialSearch:
    def __init__(self):
        # set up current board state
        pass

    def findOptimalMove(self):
        # get the current board state

        bestMove = -1
        bestValue = float('-inf')
        moves = []

        # Call minimax function on each available move
        for move in moves:
            # Create a new state where that move is performed
            # newState = State()
            # get the "value" or "score" for that move
            moveValue = self.minimax()

            if moveValue > bestValue:
                bestValue = moveValue
                bestMove = move

        # return the move with the highest evaluation
        return bestMove


def maxN(self, state, depth, playerIndex):
    """
    Implements the Max-N algorithm to evaluate the best possible move for each player in a game
    with N players, considering multiple adversaries.

    Parameters:
    - state (State object): The current game state.
    - depth (int): The depth of the game tree to explore.
    - playerIndex (int): The index of the current player (0 to N-1).

    Returns:
    - List[int]: A vector of evaluation scores for each player in the game.

    This function recursively evaluates child states by simulating moves for all players until
    the specified depth is reached or the game is over. Each player aims to maximize their own score.
    """
    numPlayers = (
        self.getNumPlayers()
    )  # Assume this method returns the number of players in the game
    if depth == 0 or self.gameOver(state):
        return self.evaluateBoard(
            state
        )  # This must now return a list of scores, one for each player

    # Initialize a score list with worst possible scores for each player
    scores = [
        float("-inf") if i == playerIndex else float("inf") for i in range(numPlayers)
    ]

    for move in state.availableMoves:
        newState = self.updateState(deepcopy(state), move)
        nextPlayerIndex = (playerIndex + 1) % numPlayers
        eval = self.maxN(newState, depth - 1, nextPlayerIndex)

        # Update the score for the current player
        if eval[playerIndex] > scores[playerIndex]:
            scores = eval  # Update all scores since this is the best move for the current player

    return scores

    def evaluateBoard(self, state):
        return 1;
