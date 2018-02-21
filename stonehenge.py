"""
An implementation of the Stonehenge game and its state.
"""
from game import Game
from game_state import GameState
from typing import Any


class StonehengeGame(Game):
    """
    The Stonehenge game.
    """
    def __init__(self, p1_starts: bool) -> None:
        """
        Initialize this Game, using p1_starts to find who the first player is.
        """
        raise NotImplementedError

    def get_instructions(self) -> str:
        """
        Return the instructions for this Game.
        """
        raise NotImplementedError

    def is_over(self, state: GameState) -> bool:
        """
        Return whether or not this game is over at state.
        """
        raise NotImplementedError

    def is_winner(self, player: str) -> bool:
        """
        Return whether player has won the game.

        Precondition: player is 'p1' or 'p2'.
        """
        raise NotImplementedError

    def str_to_move(self, string: str) -> Any:
        """
        Return the move that string represents. If string is not a move,
        return some invalid move.
        """
        raise NotImplementedError


class StonehengeState(GameState):
    """
    The state of Stonehenge at a certain point in time.
    """


if __name__ == "__main__":
    from python_ta import check_all
    check_all(config="a2_pyta.txt")
