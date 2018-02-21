"""
An implementation of the Stonehenge game and its state.
"""
from game import Game
from game_state import GameState


class StonehengeGame(Game):
    """
    The Stonehenge game.
    """


class StonehengeState(GameState):
    """
    The state of Stonehenge at a certain point in time.
    """


if __name__ == "__main__":
    from python_ta import check_all
    check_all(config="a2_pyta.txt")
