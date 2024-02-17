# Import necessary modules and functions
from Board import checkDraw, Status, checkWinner, playerMarble
from copy import deepcopy

# Allows agent to use marble chars 'X' and 'O' to pass integers to Board
playerMarbleStrings = {
    playerMarble[0]: 0,
    playerMarble[1]: 1
}

class State:
    def __init__(self, board, marble, top):
        self.board = board
        self.marble = marble # represents the next player's turn
        self.top = top
        # This keeps track of which columns are currently full
        self.availableMoves = [c for c in range(len(top)) if top[c] < len(self.board)]

class AdversarialSearch:
    def __init__(self, marble, depth):
        self.marble = marble # The maximizing players's marble
        self.depth = depth

    def findOptimalMove(self, board, top):
        currentState = State(board, self.marble, top)
        
        bestMove = -1
        bestValue = float('-inf')

        # Call minimax function on each available move
        for col in currentState.availableMoves:
            newState = self.updateState(deepcopy(currentState), col)
            moveValue = self.minimax(newState, self.depth, float('-inf'), float('inf'), False)

            if moveValue > bestValue:
                bestValue = moveValue
                bestMove = col

        # return the move with the highest evaluation
        return bestMove

    def minimax(self, state, depth, alpha, beta, maximizingPlayer):
        """
        Implements the Minimax algorithm with Alpha-Beta pruning to evaluate the best possible 
        move for a player in a given game state.

        Parameters:
        - state (State object): The current game state.
        - depth (int): The depth of the game tree to explore. A depth of 0 will return the 
        evaluation of the current state.
        - alpha (int): The best score that the maximizing player can guarantee at this level or above.
        - beta (int): The best score that the minimizing player can guarantee at this level or above.
        - maximizingPlayer (bool): True if the current player is maximizing, False if minimizing.

        Returns:
        - int: The evaluation score of the state for the current player. If the player is maximizing then 
        it returns the maximum evaluation score of the child states. If the player is minimizing then 
        it returns the minimum evaluation score of the child states.

        This function recursively evaluates child states by simulating moves for both players until
        the specified depth is reached or the game is over. It uses Alpha-Beta pruning to cut off branches in 
        the game tree and reduce the number of states evaluated.

        """
        if depth == 0 or gameOver(state):
            return self.evaluateBoard(state)
    
        if maximizingPlayer:
            maxEval = float('-inf')
            for move in state.availableMoves:
                eval = self.minimax(self.updateState(deepcopy(state), move), depth - 1, alpha, beta, False)
                maxEval = max(maxEval, eval)

                # prunning
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return maxEval
    
        else:
            minEval = float('inf')
            for move in state.availableMoves:
                eval = self.minimax(self.updateState(deepcopy(state), move), depth - 1, alpha, beta, True)
                minEval = min(minEval, eval)

                # pruning
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return minEval

    def updateState(self, state, move):
        new_board = deepcopy(state.board)
        new_top = deepcopy(state.top)

        new_board[new_top[move]][move] = state.marble
        new_top[move] += 1

        next_marble = 'O' if state.marble == 'X' else 'X'
        return State(new_board, next_marble, new_top)

    def evaluateBoard(self, state):
        OPPONENT_MARBLE = 'O' if self.marble == 'X' else 'X'  # opponent's marble

        value = 0

        # Check for immediate win/loss
        if checkWinner(state.board, playerMarbleStrings[self.marble]) == Status.Win:
            return 100
        elif checkWinner(state.board, playerMarbleStrings[OPPONENT_MARBLE]) == Status.Win:
            return -100
        elif checkDraw(state.top, len(state.board[0]), len(state.board)) == Status.Draw:
            return 0

        # Count threats
        # Counting threats for 3 marbles and 1 space
        value += 7 * count_threats_for_n(state.board, self.marble, 3)
        value -= 7 * count_threats_for_n(state.board, OPPONENT_MARBLE, 3)
        # Counting threats for 2 marbles and 2 spaces
        value += 5 * count_threats_for_n(state.board, self.marble, 2)
        value -= 5 * count_threats_for_n(state.board, OPPONENT_MARBLE, 2)
        # Counting threats for 1 marble and 3 spaces
        value += 3 * count_threats_for_n(state.board, self.marble, 1)
        value -= 3 * count_threats_for_n(state.board, OPPONENT_MARBLE, 1)

        # Optimizes for center columns
        center_columns = list(range(1, len(state.board[0]) - 1))
        for row in state.board:
            for col in center_columns:
                if row[col] == self.marble:
                    value += 1
                elif row[col] == OPPONENT_MARBLE:
                    value -= 1
            
        return value


def count_threats_for_n(board, marble, n):
    count = 0

    # Helper function to count marbles and spaces in a segment
    def check_segment(segment):
        return segment.count(marble) == n and segment.count(' ') == 4 - n

    for row in range(len(board)):
        for col in range(len(board[0])):
            # Check horizontal segments
            if col <= len(board[0]) - 4:
                segment = [board[row][col + i] for i in range(4)]
                count += check_segment(segment)
                
            # Check vertical segments
            if row <= len(board) - 4:
                segment = [board[row + i][col] for i in range(4)]
                count += check_segment(segment)
            
            # Check diagonal segments (top-left to bottom-right)
            if row <= len(board) - 4 and col <= len(board[0]) - 4:
                segment = [board[row + i][col + i] for i in range(4)]
                count += check_segment(segment)
            
            # Check diagonal segments (top-right to bottom-left)
            if row <= len(board) - 4 and col >= 3:
                segment = [board[row + i][col - i] for i in range(4)]
                count += check_segment(segment)

    return count

# Returns True if the game is over and False otherwise
def gameOver(state):
    return ((checkWinner(state.board, 0) == Status.Win)
    or (checkWinner(state.board, 1) == Status.Win) or 
    (checkDraw(state.top, len(state.board[0]), len(state.board))== Status.Draw))