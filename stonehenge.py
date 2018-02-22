"""
An implementation of the Stonehenge game and its state.
"""
from game import Game
from game_state import GameState
from typing import Any, List, Optional, Union


def create_board_dict(n: int) -> List[List[Optional[str]]]:
    """
    Create a board of size n.
    """
    letters = [chr(i) for i in range(ord('A'), ord('Z') + 1)]
    number_of_cells = int((((n + 1) * (n + 2)) / 2) - 1 + n)
    cells = letters[:number_of_cells]
    list_return = []
    for i in range(2, n + 2):
        temp = []
        for j in range(i):
            temp.append(cells.pop(0))
        list_return.append(temp)
    list_return.append(cells)
    return list_return


def score(line: List[Union[str, int]]) -> Optional[int]:
    """
    Return if player 1, 2, or none of them captured the ley-line line.
    """
    if line.count(1) >= (len(line)) / 2:
        return 1
    elif line.count(2) >= (len(line)) / 2:
        return 2
    return None


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
        instructions = "Players take turns claiming cells. When a player " \
                       "captures at least half of the cells in a ley-line, " \
                       "then the player captures that ley-line. The first " \
                       "player to capture at least half of the ley-lines is " \
                       "the winner. A ley-line, once claimed, cannot be " \
                       "taken by the other player."
        return instructions

    def is_over(self, state: "StonehengeState") -> bool:
        """
        Return whether or not this game is over at state.
        """
        ley_lines = state.get_ley_lines()
        scores = [score(line) for line in ley_lines]
        return (scores.count(1) >= (len(scores)) / 2) or (scores.count(2) >=
                                                          (len(scores)) / 2)

    def is_winner(self, player: str) -> bool:
        """
        Return whether player has won the game.

        Precondition: player is 'p1' or 'p2'.
        """
        return (self.current_state.get_current_player_name() != player
                and self.is_over(self.current_state))

    def str_to_move(self, string: str) -> Any:
        """
        Return the move that string represents. If string is not a move,
        return some invalid move.
        """
        move = string.strip()
        letters = [chr(i) for i in range(ord('A'), ord('Z') + 1)]
        n = len(self.current_state.board[0]) - 1
        number_of_cells = int((((n + 1) * (n + 2)) / 2) - 1 + n)
        cells = letters[:number_of_cells]
        if move in cells:
            return move
        return None


class StonehengeState(GameState):
    """
    The state of Stonehenge at a certain point in time.
    """
    def __init__(self, is_p1_turn: bool, board: List[List[Union[str, int, None]]], cells: str) -> None:
        """
        Initialize this game state and set the current player based on
        is_p1_turn.
        """
        super().__init__(is_p1_turn)
        self.cells = cells
        # self.board = self.create_board()

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

    def get_ley_lines(self) -> List[List[Union[str, int, None]]]:
        """
        Return a list of all the ley-lines in the board.
        """
        pass


if __name__ == "__main__":
    from python_ta import check_all
    check_all(config="a2_pyta.txt")
