"""
An implementation of the Stonehenge game and its state.
"""
from game import Game
from game_state import GameState
from typing import Any, List, Dict, Optional, Union


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

    size - the side length of the board
    current_state - the current state of the game
    """
    def __init__(self, p1_starts: bool) -> None:
        """
        Initialize this Game, using p1_starts to find who the first player is.
        """
        self.size = int(input('Enter the side length of the board: '))
        self.current_state = StonehengeState(p1_starts, self.create_cells())

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
        if type(string) is str:
            move = string.strip()
            cells = self.create_cells()
            if move in cells:
                return move
        return None

    def create_cells(self) -> List[str]:
        """
        Create a board of size self.size.
        """
        n = self.size
        letters = [chr(i) for i in range(ord('A'), ord('Z') + 1)]
        number_of_cells = int(((n ** 2) + 5 * n) / 2)
        return letters[:number_of_cells]


class StonehengeState(GameState):
    """
    The state of Stonehenge at a certain point in time.

    size - the side length of the board
    cells - the cells in the board, which can be an alphabetical character
    or 1 or 2
    board -
    """
    def __init__(self, is_p1_turn: bool, cells: List[Union[str, int]]) -> None:
        """
        Initialize this game state and set the current player based on
        is_p1_turn.
        """
        super().__init__(is_p1_turn)
        if len(cells) == 3:
            self.size = 1
        elif len(cells) == 7:
            self.size = 2
        elif len(cells) == 12:
            self.size = 3
        elif len(cells) == 18:
            self.size = 4
        elif len(cells) == 25:
            self.size = 5
        self.cells = cells
        self.board = self.create_board()

    def __str__(self) -> str:
        """
        Return a string representation of the current state of the game.
        """
        raise NotImplementedError

    def get_possible_moves(self) -> List[str]:
        """
        Return all possible moves that can be applied to this state.
        """
        return [cell for cell in self.cells if type(cell) is str]

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
        return str(self) + "\nP1's turn: {}".format(self.p1_turn)

    def rough_outcome(self) -> float:
        """
        Return an estimate in interval [LOSE, WIN] of best outcome the current
        player can guarantee from state self.
        """
        raise NotImplementedError

    def create_board(self) -> List[Dict[Union[str, int], List[Union[str, int]]]]:
        """
        Create a board of size n.
        """
        # ley_lines = self.get_ley_lines()

    def get_ley_lines(self) -> List[List[Union[str, int]]]:
        """
        Return a list of all the ley-lines in the board.
        """
        ley_lines = self.create_rows()
        rows = ley_lines[:]

        # Extracting the / ley-lines
        for i in range(self.size + 1):
            temp_list = []
            for j in range(len(rows)):
                if j != len(rows) - 1:
                    try:
                        temp_list.append(rows[j][i])
                    except IndexError:
                        pass
                else:
                    if i != 0:
                        temp_list.append(rows[j][i-1])
            ley_lines.append(temp_list)
        return ley_lines

    def create_rows(self) -> List[List[Union[str, int]]]:
        """
        Create the rows (horizontal ley-lines) from self.cells.
        """
        n = self.size
        list_return = []
        temp = 0
        for i in range(2, n + 2):
            list_return.append(self.cells[temp:temp + i])
            temp += i
        list_return.append(self.cells[len(self.cells) - n:])
        return list_return


if __name__ == "__main__":
    from python_ta import check_all
    check_all(config="a2_pyta.txt")
