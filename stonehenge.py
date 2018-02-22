"""
An implementation of the Stonehenge game and its state.
"""
from game import Game
from game_state import GameState
from typing import Any, Dict


def create_board_dict(side_length: int) -> Dict[str, str]:
    """Create a dictionary of the board based on side_length."""
    letters = [chr(i) for i in range(ord('A'), ord('Z') + 1)]


class StonehengeGame(Game):
    """
    The Stonehenge game.

    p1_starts - the starting player of the game
    current_state - the current state of the game
    """
    def __init__(self, p1_starts: bool) -> None:
        """
        Initialize this Game, using p1_starts to find who the first player is.
        """
        board = create_board_dict(int(input('Enter the side length '
                                            'of the board: ')))
        self.current_state = StonehengeState(p1_starts, board)

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
    def __init__(self, is_p1_turn: bool, board: Dict[str, str]) -> None:
        """
        Initialize this game state and set the current player based on
        is_p1_turn.
        """
        super().__init__(is_p1_turn)
        self.board = board

    def __str__(self) -> str:
        """
        Return a string representation of the current state of the game.
        """
        raise NotImplementedError

    def get_possible_moves(self) -> list:
        """
        Return all possible moves that can be applied to this state.
        """
        raise NotImplementedError

    def make_move(self, move: Any) -> 'GameState':
        """
        Return the GameState that results from applying move to this GameState.
        """
        raise NotImplementedError

    def __repr__(self) -> Any:
        """
        Return a representation of this state (which can be used for
        equality testing).
        """
        raise NotImplementedError

    def rough_outcome(self) -> float:
        """
        Return an estimate in interval [LOSE, WIN] of best outcome the current
        player can guarantee from state self.
        """
        raise NotImplementedError

if __name__ == "__main__":
    from python_ta import check_all
    check_all(config="a2_pyta.txt")
