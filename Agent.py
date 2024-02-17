from copy import deepcopy


def find_snake_by_name(snakes, snake_name):
    # Search for a snake with the given name in the list of Snake instances
    for index, snake in enumerate(snakes):
        if snake.name == snake_name:
            return index
    return None

class State:

    def __init__(self, board, snakes, height, width, numPlayers, food):
        # reference to the current state of the game board
        self.board = board
        self.snakes = snakes
        self.height = height
        self.width = width
        self.numPlayers = numPlayers
        self.food = food

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



    def availableMoves(self, snake_name):
        """Returns a list of available moves for the snake, considering wall, self, and other snakes" collisions."""
        # We've included code to prevent your Battlesnake from moving backwards
        is_move_safe = {"up": True, "down": True, "left": True, "right": True}
        snake = self.snakes[find_snake_by_name(self.snakes, snake_name)]
        my_head = snake.body[0]  # Coordinates of your head
        my_neck = snake.body[1]  # Coordinates of your "neck"

        if my_neck["x"] < my_head["x"]:  # Neck is left of head, don't move left
            is_move_safe["left"] = False

        elif my_neck["x"] > my_head["x"]:  # Neck is right of head, don't move right
            is_move_safe["right"] = False

        elif my_neck["y"] < my_head["y"]:  # Neck is below head, don't move down
            is_move_safe["down"] = False

        elif my_neck["y"] > my_head["y"]:  # Neck is above head, don't move up
            is_move_safe["up"] = False

        # Prevent your Battlesnake from moving out of bounds
        board_width = self.width
        board_height = self.height

        # If head is at the left edge, cannot move left
        if my_head["x"] == 0:
            is_move_safe["left"] = False

        # If head is at the right edge, cannot move right
        if my_head["x"] == board_width - 1:
            is_move_safe["right"] = False

        # If head is at the bottom edge, cannot move down
        if my_head["y"] == 0:
            is_move_safe["down"] = False

        # If head is at the top edge, cannot move up
        if my_head["y"] == board_height - 1:
            is_move_safe["up"] = False

        # Prevent your Battlesnake from colliding with itself
        my_body = snake.body

        ## Do not move into the body of the snake
        for segment in my_body[2:]: # Skip head

            # Is segment to left of head
            if segment["x"] == my_head["x"] - 1 and segment["y"] == my_head["y"]: 
                is_move_safe["left"] = False

            # Is segment to right of head
            if segment["x"] == my_head["x"] + 1 and segment["y"] == my_head["y"]:
                is_move_safe["right"] = False

            # Is segment above head
            if segment["y"] == my_head["y"] + 1 and segment["x"] == my_head["x"]:
                is_move_safe["up"] = False

            # Is segment below head
            if segment["y"] == my_head["y"] - 1 and segment["x"] == my_head["x"]:
                is_move_safe["down"] = False

        # Prevent your Battlesnake from colliding with other Battlesnakes
        opponents = self.snakes

        # Loop through each opponent snake
        for opponent in opponents:
            # Loop through each body segment of the opponent snake (excluding the tail since it moves)
            for segment in opponent.body:
                # Check if a segment is directly left of my snake's head
                if segment["x"] == my_head["x"] - 1 and segment["y"] == my_head["y"]:
                    is_move_safe["left"] = False
                # Check if a segment is directly right of my snake's head
                if segment["x"] == my_head["x"] + 1 and segment["y"] == my_head["y"]:
                    is_move_safe["right"] = False
                # Check if a segment is directly above my snake's head
                if segment["x"] == my_head["x"] and segment["y"] == my_head["y"] + 1:
                    is_move_safe["up"] = False
                # Check if a segment is directly below my snake's head
                if segment["x"] == my_head["x"] and segment["y"] == my_head["y"] - 1:
                    is_move_safe["down"] = False

        safe_moves = []
        for move, isSafe in is_move_safe.items():
            if isSafe:
                safe_moves.append(move)
        return safe_moves

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
        self.snakes = [Snake(snake) for snake in board["snakes"]]
        height = board["height"]
        width = board["height"]
        self.numPlayers = len(self.snakes)
        food = [food for food in board["food"]]
        self.initial_state = State(board, self.snakes, height, width, self.numPlayers, food)
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

            values = self.maxN(newState, 3, find_snake_by_name(self.snakes, self.you.name))
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

        for move in state.availableMoves(snake_name=state.snakes[playerIndex].name):
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
        print(scores)
        return scores

    def manhattanDistance(self, p1, p2):
        # Note: p1 and p2 are now expected to be dictionaries with "x" and "y" keys
        return abs(p1["x"] - p2["x"]) + abs(p1["y"] - p2["y"])
