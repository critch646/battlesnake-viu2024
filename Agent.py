from copy import deepcopy

class State:

    def __init__(self, board, snakes, height, width, numPlayers, food):
        # reference to the current state of the game board
        self.board = board
        self.snakes = snakes
        self.height = height
        self.width = width
        self.numPlayers = numPlayers
        self.food = food
        self.availableMoves = ["up", "down", "left", "right"]

    def updateState(self, move, snake_name):
        """Updates current state with the move applied to the snake. Caller responsible for making copy of state."""

        # iterate through snakes and update the snake with the move, also update health
        for snake in self.snakes:
            snake.health -= 1

            if snake.name == snake_name:
                snake.body = move
                snake.head = move[0]

        # check if any snakes have collided
        self.checkCollisions()

    def checkCollisions(self):
        """Checks if any snakes have collided and removes them from the state if they have."""
        """Checks if any snakes have collided and updates the state accordingly."""
        to_remove = set()

        # Check for wall collisions and self-collisions
        for snake in self.snakes:
            if (snake.head["x"] < 0 or snake.head["x"] >= self.width or
                snake.head["y"] < 0 or snake.head["y"] >= self.height or
                snake.head in [segment for segment in snake.body[1:]]):
                to_remove.add(snake)

        # Check for collisions with other snakes
        for snake in self.snakes:
            if snake in to_remove:
                continue
            for other_snake in self.snakes:
                if snake != other_snake:
                    # Check for head-to-head collisions
                    if snake.head == other_snake.head:
                        # Remove the shorter snake or both if equal length
                        if snake.length <= other_snake.length:
                            to_remove.add(snake)
                        if snake.length >= other_snake.length:
                            to_remove.add(other_snake)
                    # Check for head-to-body collisions
                    elif snake.head in other_snake.body:
                        to_remove.add(snake)

        # Remove collided snakes
        for snake in to_remove:
            self.snakes.remove(snake)

        # Check for food consumption
        for snake in self.snakes:
            if snake.head in self.food:
                self.food.remove(snake.head)
                snake.health = 100
                snake.length += 1


class Snake:
    def __init__(self, snake):
        self.name = snake["name"]
        self.health = snake["health"]
        self.body = snake["body"]
        self.head = snake["head"]
        self.length = snake["length"]


class AdversarialSearch:
    def __init__(self, game):
        # set up current board state
        board = game["board"]
        snakes = [Snake(snake) for snake in board["snakes"]]
        height = board["height"]
        width = board["height"]
        self.numPlayers = len(snakes)
        food = [food for food in board["food"]]
        self.initial_state = State(board, snakes, height, width, self.numPlayers, food)
        self.you = Snake(game["you"])

    def findOptimalMove(self, safeMoves):
        # get the current board state

        bestMove = -1
        bestValue = float('-inf')

        # Call minimax function on each available move
        for move in safeMoves:
            # Create a new state where that move is performed
            newState = deepcopy(self.initial_state)
            newState.updateState(self.you, move)
            # get the "value" or "score" for that move
            values = self.maxN(newState, 3, self.numPlayers-1)
            print("VALUES", values)
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
            ev = GameEvaluator(state)
            return ev.evaluateBoard()  # This must now return a list of scores, one for each player

        # Initialize all players' scores to -inf, as each actual score will be an improvement
        scores = [float("-inf") for _ in range(numPlayers)]

        print(playerIndex)

        for move in state.availableMoves:
            newState = State(
                state.board,
                state.snakes,
                state.height,
                state.width,
                state.numPlayers,
                state.food,
            )
            newState.updateState(playerIndex, move)
            # Here, you need to correctly implement move simulation on newState based on the given move
            # For example, you might have newState.simulateMove(move, playerIndex) or similar

            nextPlayerIndex = (playerIndex + 1) % numPlayers
            newDepth = depth - 1 if nextPlayerIndex == 0 else depth
            newScores = self.maxN(newState, newDepth, nextPlayerIndex)

            # This checks if the evaluated score for the current player is better than what was previously found
            # If so, it updates the scores for all players based on this move's outcome
            if newScores[nextPlayerIndex] > scores[nextPlayerIndex]:
                scores = newScores  # Update the scores to reflect the best outcome found for this move

        return scores

    def gameOver(self, state):
        return len(state.snakes) <= 1


class GameEvaluator:
    def __init__(self, state):
        self.state = state

    def evaluateBoard(self):
        scores = [0] * self.state.numPlayers  # Initialize scores for each snake

        # Evaluate various aspects of the game state
        scores = self.evaluateFood(scores)
        scores = self.evaluateWalls(scores)
        scores = self.evaluateSnakesCollision(scores)
        scores = self.evaluateHeadOnCollisions(scores)

        return scores

    def evaluateFood(self, scores):
        for i, snake in enumerate(self.state.snakes):
            head = snake.head  # Assuming the head is the first element
            if len(self.state.food) > 0:  # Ensure there is food to consider
                distance_to_closest_food = min(
                    [self.manhattanDistance(head, food) for food in self.state.food]
                )
                # Closer to food is better, inverse relation
                scores[i] += max(0, 10 - distance_to_closest_food)
        return scores

    def evaluateWalls(self, scores):
        for i, snake in enumerate(self.state.snakes):
            head = snake.head
            # Penalize positions closer to walls
            distance_to_wall = min(
                [
                    head["x"],
                    self.state.width - head["x"] - 1,
                    head["y"],
                    self.state.height - head["y"] - 1,
                ]
            )
            scores[i] += max(
                0, distance_to_wall - 1
            )  # Closer than 1 block to wall is bad
        return scores

    def evaluateSnakesCollision(self, scores):
        for i, snake in enumerate(self.state.snakes):
            head = snake.head
            # Check potential collisions with other snakes and itself
            for j, other_snake in enumerate(self.state.snakes):
                if i != j:  # Avoid self
                    if head in [segment for segment in other_snake.body[1:]]:
                        scores[i] -= 10  # Penalize for potential collision
        return scores

    def evaluateHeadOnCollisions(self, scores):
        for i, snake in enumerate(self.state.snakes):
            head = snake.head
            for j, other_snake in enumerate(self.state.snakes):
                if i != j:
                    other_head = other_snake.head
                    if self.manhattanDistance(head, other_head) == 1:
                        # Predict head-on collision, could refine to check direction
                        scores[i] -= 5
        return scores

    def manhattanDistance(self, p1, p2):
        # Note: p1 and p2 are now expected to be dictionaries with "x" and "y" keys
        return abs(p1["x"] - p2["x"]) + abs(p1["y"] - p2["y"])
