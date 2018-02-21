"""
A module for strategies.

NOTE: Make sure this file adheres to python-ta.
Adjust the type annotations as needed, and implement both a recursive
and an iterative version of minimax.
"""
from typing import Any


# TODO: Adjust the type annotation as needed.
def interactive_strategy(game: Any) -> Any:
    """
    Return a move for game through interactively asking the user for input.
    """
    move = input("Enter a move: ")
    return game.str_to_move(move)

# TODO: Implement a recursive version of the minimax strategy.

# TODO: Implement an iterative version of the minimax strategy.


if __name__ == "__main__":
    from python_ta import check_all

    check_all(config="a2_pyta.txt")
