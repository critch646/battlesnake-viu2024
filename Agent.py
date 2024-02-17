from copy import deepcopy

class State:
    def __init__(self, game):
        # reference to the current state of the game board
        self.board = game["board"]
        self.snakes = [Snake(snake) for snake in game["snakes"]]
        self.height = self.board["height"]
        self.width = self.board["height"]
        self.numPlayers = len(self.snakes)
        self.food = [food for food in self.board["food"]]

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

        def availableMoves(self, snake_name):
            """Returns a list of available moves for the snake, considering wall, self, and other snakes' collisions."""
            snake = next((s for s in self.snakes if s.name == snake_name), None)
            if snake is None:
                return []

            potential_moves = {
                'up': {"x": snake.head["x"], "y": snake.head["y"] + 1},
                'down': {"x": snake.head["x"], "y": snake.head["y"] - 1},
                'left': {"x": snake.head["x"] - 1, "y": snake.head["y"]},
                'right': {"x": snake.head["x"] + 1, "y": snake.head["y"]}
            }

            valid_moves = []

            for direction, move in potential_moves.items():
                if 0 <= move["x"] < self.width and 0 <= move["y"] < self.height:
                    # Self-collision
                    if any(segment['x'] == move['x'] and segment['y'] == move['y'] for segment in snake.body[:-1]):
                        continue

                    # Other sneks collision
                    collision_with_other_snake = False
                    for other_snake in self.snakes:
                        if other_snake.name != snake_name:
                            if any(segment['x'] == move['x'] and segment['y'] == move['y'] for segment in other_snake.body):
                                collision_with_other_snake = True
                                break
                    
                    if not collision_with_other_snake:
                        valid_moves.append(direction)

            return valid_moves





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
            eval = self.maxN(newState, depth - 1, nextPlayerIndex)

            # Update the score for the current player
            if eval[playerIndex] > scores[playerIndex]:
                scores = eval  # Update all scores since this is the best move for the current player

        return scores

    def evaluateBoard(self):
        return 1;

    def gameOver(self, state):
        return len(state.snakes) == 0 or self.you.health == 0
