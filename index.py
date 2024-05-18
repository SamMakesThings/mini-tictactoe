# Small script for Recurse application

import copy

state = [[None, None, None], [None, None, None], [None, None, None]]


def state_updater(state: list, move_str: str) -> list:
    # pure function to calculate a new state based on move
    # move_str takes the format of a 3-char str, "x y player"
    # x and y are the coordinates of the action
    # player is either x or o
    # spaces to split

    x, y, player = move_str.split(" ")
    x = int(x)
    y = int(y)

    # validate state
    # check x indexes
    if len(state) != 3:  # check x index lengths
        raise ValueError(f"Invalid game state: Wrong row length of {len(state)}")
    # check y indexes
    if len([False for x in state if len(x) != 3]) != 0:
        raise ValueError("Invalid game state: Wrong column length")
    # check for invalid values
    if len([False for x in state for y in x if y not in ["x", "y", None]]) != 0:
        raise ValueError(f"Invalid game state: Incorrect value in state: {y}")

    # validate move
    if x < 0 or x > 2:
        raise ValueError(f"Invalid move: {x} is not a valid x index")
    if y < 0 or y > 2:
        raise ValueError(f"Invalid move: {y} is not a valid y index")
    if player not in ["x", "o"]:
        raise ValueError(f"Invalid move: {player} is not a valid player")

    selected_square = state[x][y]

    if selected_square is not None:
        raise ValueError(f"Invalid move: Square {x} {y} is already occupied")

    # make the confirmed valid move
    new_state = copy.deepcopy(state)
    new_state[x][y] = player

    return new_state
