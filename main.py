# Welcome to
# __________         __    __  .__                               __
# \______   \_____ _/  |__/  |_|  |   ____   ______ ____ _____  |  | __ ____
#  |    |  _/\__  \\   __\   __\  | _/ __ \ /  ___//    \\__  \ |  |/ // __ \
#  |    |   \ / __ \|  |  |  | |  |_\  ___/ \___ \|   |  \/ __ \|    <\  ___/
#  |________/(______/__|  |__| |____/\_____>______>___|__(______/__|__\\_____>
#
# This file can be a nice home for your Battlesnake logic and helper functions.
#
# To get you started we've included code to prevent your Battlesnake from moving backwards.
# For more info see docs.battlesnake.com

import random
import typing
from Agent import AdversarialSearch


# info is called when you create your Battlesnake on play.battlesnake.com
# and controls your Battlesnake's appearance
# TIP: If you open your Battlesnake URL in a browser you should see this data
def info() -> typing.Dict:
    print("INFO")

    return {
        "apiversion": "1",
        "author": "csci490ftw",
        "color": "#472b5e",
        "head": "evil",
        "tail": "default",
    }


# start is called when your Battlesnake begins a game
def start(game_state: typing.Dict):
    print("GAME START")


# end is called when your Battlesnake finishes a game
def end(game_state: typing.Dict):
    print("GAME OVER\n")


# move is called on every turn and returns your next move
# Valid moves are "up", "down", "left", or "right"
# See https://docs.battlesnake.com/api/example-move for available data
def move(game_state: typing.Dict) -> typing.Dict:
    print("game_state:", game_state)
    is_move_safe = {"up": True, "down": True, "left": True, "right": True}

    # We've included code to prevent your Battlesnake from moving backwards
    my_head = game_state["you"]["body"][0]  # Coordinates of your head
    my_neck = game_state["you"]["body"][1]  # Coordinates of your "neck"

    if my_neck["x"] < my_head["x"]:  # Neck is left of head, don't move left
        is_move_safe["left"] = False

    elif my_neck["x"] > my_head["x"]:  # Neck is right of head, don't move right
        is_move_safe["right"] = False

    elif my_neck["y"] < my_head["y"]:  # Neck is below head, don't move down
        is_move_safe["down"] = False

    elif my_neck["y"] > my_head["y"]:  # Neck is above head, don't move up
        is_move_safe["up"] = False

    # Prevent your Battlesnake from moving out of bounds
    board_width = game_state['board']['width']
    board_height = game_state['board']['height']

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
    my_body = game_state['you']['body']

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
    opponents = game_state['board']['snakes']

    # Loop through each opponent snake
    for opponent in opponents:
        # Loop through each body segment of the opponent snake (excluding the tail since it moves)
        for segment in opponent["body"][:-1]:
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

    # Are there any safe moves left?
    safe_moves = []
    for move, isSafe in is_move_safe.items():
        if isSafe:
            safe_moves.append(move)

    if len(safe_moves) == 0:
        print(f"MOVE {game_state['turn']}: No safe moves detected! Moving down")
        return {"move": "down"}

    # Choose a random move from the safe ones
    next_move = random.choice(safe_moves)

    agent = AdversarialSearch(game=game_state)
    next_move = agent.findOptimalMove(safeMoves=safe_moves)

    # Food check
    if len(safe_moves) > 1:
        foods = game_state["board"]["food"]

        ## is a safe move food?
        for food in foods:
            for move in safe_moves:
                if move == "up" and food["y"] == my_head["y"] + 1 and food["x"] == my_head["x"]:
                    next_move = "up"
                    break
                elif move == "down" and food["y"] == my_head["y"] - 1 and food["x"] == my_head["x"]:
                    next_move = "down"
                    break
                elif move == "right" and food["x"] == my_head["x"] + 1 and food["y"] == my_head["y"]:
                    next_move = "right"
                    break
                elif move == "left" and food["x"] == my_head["x"] - 1 and food["y"] == my_head["y"]:
                    next_move = "left"
                    break

    print(f"MOVE {game_state['turn']}: {next_move}")
    return {"move": next_move}


# Start server when `python main.py` is run
if __name__ == "__main__":
    from server import run_server

    run_server({"info": info, "start": start, "move": move, "end": end})
