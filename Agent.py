from copy import deepcopy

class State:
    def __init__(self, game):
        # reference to the current state of the game board
        self.board = game["board"]
        self.snakes = [Snake(snake) for snake in game["snakes"]]
        self.snakes.append(Snake(game["you"]))
        self.height = self.board["height"]
        self.width = self.board["height"]
        self.numPlayers = len(self.snakes)


class Snake:
    def __init__(self, snake):
        self.name = snake["name"]
        self.health = snake["health"]
        self.body = snake["body"]
        self.head = snake["head"]
        self.length = snake["length"]


class AdversarialSearch:
    def __init__(self, board):
        # set up current board state
        self.initial_state = State(board)
        self.you = Snake(board["you"])
        pass

    def findOptimalMove(self, safeMoves):
        # get the current board state

        bestMove = -1
        bestValue = float('-inf')

        # Call minimax function on each available move
        for move in safeMoves:
            # Create a new state where that move is performed
            newState = State(self.initial_state)
            newState.updateState(self.you, move)
            # get the "value" or "score" for that move
            values = self.maxN(self, newState, 3, self.numPlayers)
            moveValue = values[-1] # our snake

            if moveValue > bestValue:
                bestValue = moveValue
                bestMove = move

        # return the move with the highest evaluation
        return bestMove

    def maxN(self, state: State, depth, playerIndex):
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
        numPlayers = len(state.snakes)
        if depth == 0 or self.gameOver(state):
            return self.evaluateBoard(state)  # This must now return a list of scores, one for each player

        # Initialize a score list with worst possible scores for each player
        scores = [
            float("-inf") if i == playerIndex else float("inf") for i in range(numPlayers)
        ]

        for move in state.availableMoves:
            newState = self.updateState(deepcopy(state), move)
            nextPlayerIndex = (playerIndex + 1) % numPlayers
            newDepth = depth - 1 if nextPlayerIndex == 0 else depth
            eval = self.maxN(newState, newDepth, nextPlayerIndex)

            # Update the score for the current player
            if eval[playerIndex] > scores[playerIndex]:
                scores = eval  # Update all scores since this is the best move for the current player

        return scores

    def evaluateBoard(self):
        return 1;

    def gameOver(self, state):
        return len(state.snakes) == 0 or self.you.health == 0
