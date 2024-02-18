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

    def updateState(self, direction, snake_name):
        # Find the snake to update
        for snake in self.snakes:
            if snake.name == snake_name:
                # Calculate new head based on the direction
                new_head = dict(snake.head)  # Make a copy to avoid direct modification
                if direction == "up":
                    new_head["y"] += 1
                elif direction == "down":
                    new_head["y"] -= 1
                elif direction == "left":
                    new_head["x"] -= 1
                elif direction == "right":
                    new_head["x"] += 1

                # Update the snake's position
                snake.head = new_head
                snake.body.insert(0, new_head)  # Add new head to the body
                snake.body.pop()  # Remove the last segment to simulate movement

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
        """Returns a list of available moves for the snake, considering wall, self, and other snakes" collisions."""
        snake = next((s for s in self.snakes if s.name == snake_name), None)
        if snake is None:
            return []

        potential_moves = {
            "up": {"x": snake.head["x"], "y": snake.head["y"] + 1},
            "down": {"x": snake.head["x"], "y": snake.head["y"] - 1},
            "left": {"x": snake.head["x"] - 1, "y": snake.head["y"]},
            "right": {"x": snake.head["x"] + 1, "y": snake.head["y"]}
        }

        valid_moves = []

        for direction, move in potential_moves.items():
            if 0 <= move["x"] < self.width and 0 <= move["y"] < self.height:
                # Self-collision
                if any(segment["x"] == move["x"] and segment["y"] == move["y"] for segment in snake.body[:-1]):
                    continue

                # Other sneks collision
                collision_with_other_snake = False
                for other_snake in self.snakes:
                    if other_snake.name != snake_name:
                        if any(segment["x"] == move["x"] and segment["y"] == move["y"] for segment in other_snake.body[:-1]):
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
        newState = deepcopy(self.initial_state)
        # Now, safeMoves is already provided as an argument, so we don't need to calculate it again.
        
        bestMove = None
        bestValue = float("-inf")

        for move in safeMoves:
            # Simulate the move and evaluate
            simulatedState = deepcopy(newState)
            simulatedState.updateState(move, self.you.name)
            scores = self.evaluateBoard(simulatedState)  # This returns a list of scores for each snake
            

            moveValue = scores[0] 
            
            if moveValue > bestValue:
                bestValue = moveValue
                bestMove = move

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
        print("SCORES", scores)
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
            newState.updateState(deepcopy(state), move)
            nextPlayerIndex = (playerIndex + 1) % numPlayers
            newDepth = depth - 1 if nextPlayerIndex == 0 else depth
            eval = self.maxN(newState, newDepth, nextPlayerIndex)

            # Update the score for the current player
            scores[playerIndex] = max(scores[playerIndex], eval[playerIndex])
            print("BEST SCORES2", scores)

        print("BEST SCORES", scores)
        return scores

    def evaluateBoard(self, state):
        scores = []

        for snake in state.snakes:
            score = 0
            
            # Health Points: More health, higher score
            score += snake.health
            
            # Length: Longer might be better to a point
            score += snake.length * 2
            
            # Proximity to Food: Closer food, higher score
            closest_food_distance = min(
                abs(snake.head["x"] - food["x"]) + abs(snake.head["y"] - food["y"])
                for food in state.food
            ) if state.food else 100 
            score -= closest_food_distance

            # accessible_area = state.accessible_area(snake.head)
            # # Penalize the score based on the lack of accessible area (simplified example)
            # if accessible_area < 2:  # If less than 2 accessible cells, it might be getting trapped
            #     score -= 50  # Penalize for potential blocking off
            
            # Adjust for potential collisions (as an example, simplified)
            if (snake.head["x"] < 0 or snake.head["x"] >= state.width or
                snake.head["y"] < 0 or snake.head["y"] >= state.height):
                score -= 500
            
            scores.append(score)
        
        return scores
    
    def accessible_area(self, snake_head):
        """Calculate the number of immediately accessible cells around the snake's head."""
        accessible_cells = 0
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # Up, Right, Down, Left
        for dx, dy in directions:
            nx, ny = snake_head['x'] + dx, snake_head['y'] + dy
            if 0 <= nx < self.width and 0 <= ny < self.height:
                if not any(segment['x'] == nx and segment['y'] == ny for snake in self.snakes for segment in snake.body):
                    accessible_cells += 1
        return accessible_cells

    def gameOver(self, state):
        return len(state.snakes) <=1
