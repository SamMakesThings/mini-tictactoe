# Small script for Recurse application
import copy
from typing import Union

state = [[None, None, None], [None, None, None], [None, None, None]]


def validate_state(state: list) -> bool:
    # validate state
    # check x indexes
    if len(state) != 3:  # check x index lengths
        raise ValueError(f"Invalid game state: Wrong row length of {len(state)}")
    # check y indexes
    if len([False for x in state if len(x) != 3]) != 0:
        raise ValueError("Invalid game state: Wrong column length")
    # check for invalid values
    invalid_values = [
        val for row in state for val in row if val not in ["x", "o", None]
    ]
    if invalid_values:
        raise ValueError(
            f"Invalid game state: Incorrect player value in state: {invalid_values[0]}"
        )

    return True


def create_new_state_from_move(state: list, move_str: str) -> list:
    # pure function to calculate a new state based on move
    # move_str takes the format of a 3-char str, "x y player"
    # x and y are the coordinates of the action
    # player is either x or o
    # spaces to split

    x, y, player = move_str.split(" ")
    x = int(x)
    y = int(y)

    validate_state(state)

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


def check_rows_winner(state: list) -> Union[str, bool]:
    # assumes state is valid
    winner = [row[0] for row in state if row[0] is not None and row.count(row[0]) == 3]
    return winner[0] if winner else bool(winner)


def check_state_winner(state: list) -> Union[str, bool]:
    # pure function to determine if winner given game state
    # assumes state is valid

    # check rows
    rows_winner = check_rows_winner(state)
    if rows_winner:
        return rows_winner

    # check columns by inverting the 2d list
    inverted_state = [list(col) for col in zip(*state)]
    cols_winner = check_rows_winner(inverted_state)
    if cols_winner:
        return cols_winner

    # check diagonals
    diag1 = [row[row_index] for row_index, row in enumerate(state)]
    diag2 = [row[abs(row_index - 2)] for row_index, row in enumerate(state)]
    diags_winner = check_rows_winner([diag1, diag2])
    if diags_winner:
        return diags_winner

    return False


def render_state(state: list) -> str:
    # input state, output multiline string

    output = """---------\n"""

    for row in state:
        formatted_row = [" " if not val else val for val in row]
        output += " | ".join(formatted_row) + "\n"
        output += "---------\n"

    return output


def main():
    initial_state = [[None, None, None], [None, None, None], [None, None, None]]

    state = copy.deepcopy(initial_state)
    player_turn = "x"

    print('Welcome to tic-tac-toe! Enter your move in "<row> <column>" format ("0 2")')

    while not (winner := check_state_winner(state)):
        print(render_state(state))

        print(f"It is player {player_turn}'s turn.")

        player_input = input(
            'Please enter your move, in x y coordinates (like "0 2"): '
        )

        try:
            new_state = create_new_state_from_move(
                state, f"{player_input} {player_turn}"
            )
        except BaseException as e:
            print(f"There was an error with your input. Please try again. {e}")
            continue

        state = new_state

        player_turn = "x" if player_turn == "o" else "o"

    print(render_state(state))
    print(f"We have a winner! {winner} wins!")

    return None
