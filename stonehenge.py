"""
An implementation of the Stonehenge game and its state.
"""
from typing import Any, List, Union
from game import Game
from game_state import GameState


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
        self.current_state = StonehengeState(p1_starts, self.create_cells(),
                                             ['@'] * (3 * self.size + 3))

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
        scores = self.current_state.ley_line_scores
        return (scores.count(1) >= len(scores) / 2) or (scores.count(2) >=
                                                        len(scores) / 2)

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
            move = string.strip().upper()
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
    ley_line_scores - a list of the scores for each ley-line, where each element
    is either 1, 2, or '@' if the ley-line is unclaimed. The first element
    coressponds to the top-most left ley-line and the next ley-line in the
    clockwise direction coressponds to the next element in the list.
    """
    def __init__(self, is_p1_turn: bool, cells: List[Union[str, int]],
                 ley_line_scores: List[Union[str, int]]) -> None:
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
        self.ley_line_scores = ley_line_scores

    def __str__(self) -> str:
        """
        Return a string representation of the current state of the game.

        >>> cells = [chr(i) for i in range(ord('A'), ord('L'))]
        >>> cells.append(1)
        >>> a = StonehengeState(True, cells, [1, 2, 1, 1, 2, 1, \
1, '@', 1, 2, '@', 1])
        >>> print(a)
        """
        rows = self.extract_rows(self.cells)
        rows_to_str = []
        for row in rows:
            rows_to_str.append([str(i) for i in row])
        section_length = int(len(self.ley_line_scores) / 3)
        row_line_scores = self.ley_line_scores[section_length * 2:]
        row_line_scores.reverse()
        down_left_scores = self.ley_line_scores[:section_length]
        down_right_scores = self.ley_line_scores[
                            section_length:section_length * 2]
        down_right_scores.reverse()

        str_return = ' '*(((len(rows_to_str)-2) * 2) + 6)
        for i in range(2):
            str_return += f'{down_left_scores[i]}   '
        str_return += '\n'
        str_return += ' '*(((len(rows_to_str)-2) * 2) + 5) + '/   '*2

        for i in range(len(rows_to_str) - 1):
            row = rows_to_str[i]
            temp = ''
            for cell in row:
                temp += cell + ' - '
            str_return = str_return + '\n' + ' '*(((len(rows_to_str)-2)-i) * 2) + f'{row_line_scores[i]} - ' + temp.rstrip(' - ')
            if i != len(rows_to_str) - 2:
                str_return += f'   {down_left_scores[i + 2]}'
            str_return += '\n' + '-'*20
        temp = ''
        num_spaces = ((len(rows_to_str)-2) - (len(rows_to_str) - 3)) * 2
        for cell in rows_to_str[-1]:
            temp += cell + ' - '
        str_return = str_return + '\n' + ' ' * num_spaces + f'{row_line_scores[-1]} - ' + temp.rstrip(' - ') + f'   {down_right_scores[-1]}'

        str_return += '\n' + ' ' * (num_spaces + 5) + '\\   '*self.size
        str_return = str_return.rstrip()
        str_return += '\n' + ' ' * (num_spaces + 6)
        for i in range(self.size):
            str_return += f'{down_right_scores[i]}   '
        str_return = str_return.rstrip()
        return str_return.lstrip('\n')

    def get_possible_moves(self) -> List[str]:
        """
        Return all possible moves that can be applied to this state.
        """
        return [cell for cell in self.cells if type(cell) is str]

    def make_move(self, move: Any) -> 'StonehengeState':
        """
        Return the GameState that results from applying move to this GameState.

        >>> cells = [chr(i) for i in range(ord('A'), ord('H'))]
        >>> a = StonehengeState(True, cells, ['@'] * 9)
        >>> b = a.make_move('A')
        >>> b.p1_turn
        False
        >>> b.cells
        [1, 'B', 'C', 'D', 'E', 'F', 'G']
        >>> b.ley_line_scores
        [1, '@', '@', '@', '@', '@', '@', '@', 1]
        >>> c = b.make_move('B')
        >>> c.p1_turn
        True
        >>> c.cells
        [1, 2, 'C', 'D', 'E', 'F', 'G']
        >>> c.ley_line_scores
        [1, '@', '@', 2, '@', '@', '@', '@', 1]
        """
        current_player = int(self.get_current_player_name()[1])
        cells = self.cells[:]
        cells[cells.index(move)] = current_player
        ley_lines = self.get_ley_lines(cells)
        ley_lines_scores = self.ley_line_scores[:]

        for i in range(len(ley_lines)):
            if type(ley_lines_scores[i]) is str:
                line = ley_lines[i]
                if line.count(1) >= len(line) / 2:
                    ley_lines_scores[i] = 1
                elif line.count(2) >= len(line) / 2:
                    ley_lines_scores[i] = 2
        return StonehengeState(not self.p1_turn, cells, ley_lines_scores)

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
        pass

    def get_ley_lines(self, cells: List[Union[str, int]]) -> \
            List[List[Union[str, int]]]:
        """
        Return a list of all the ley-lines in the board based on cells.

        >>> cells = [chr(i) for i in range(ord('A'), ord('M'))]
        >>> a = StonehengeState(True, cells, ['@'] * 12)
        >>> a.get_ley_lines(cells)
        [['A', 'C', 'F'], ['B', 'D', 'G', 'J'], ['E', 'H', 'K'], ['I', 'L'], \
['B', 'E', 'I'], ['A', 'D', 'H', 'L'], ['C', 'G', 'K'], ['F', 'J'], \
['J', 'K', 'L'], ['F', 'G', 'H', 'I'], ['C', 'D', 'E'], ['A', 'B']]
        >>> cells = [chr(i) for i in range(ord('A'), ord('H'))]
        >>> a = StonehengeState(True, cells, ['@'] * 9)
        >>> a.get_ley_lines(cells)
        [['A', 'C'], ['B', 'D', 'F'], ['E', 'G'], ['B', 'E'], ['A', 'D', 'G'], \
['C', 'F'], ['F', 'G'], ['C', 'D', 'E'], ['A', 'B']]
        >>> cells = [chr(i) for i in range(ord('A'), ord('D'))]
        >>> a = StonehengeState(True, cells, ['@'] * 6)
        >>> a.get_ley_lines(cells)
        [['A'], ['B', 'C'], ['B'], ['A', 'C'], ['C'], ['A', 'B']]
        """
        ley_lines = []
        ley_lines.extend(self.extract_diagonal_ley_lines(cells, '/'))
        ley_lines.extend(self.extract_diagonal_ley_lines(cells, '\\'))
        ley_lines.extend(list(reversed(self.extract_rows(cells))))
        return ley_lines

    def extract_rows(self, cells: List[Union[str, int]]) -> \
            List[List[Union[str, int]]]:
        """
        Return the rows (horizontal ley-lines) from cells.
        """
        n = self.size
        list_return = []
        temp = 0
        for i in range(2, n + 2):
            list_return.append(cells[temp:temp + i])
            temp += i
        list_return.append(cells[-n:])
        return list_return

    def extract_diagonal_ley_lines(self, cells: List[Union[str, int]],
                                   type_: str) -> List[List[Union[str, int]]]:
        """
        Return the down-left or down-right ley-lines from cells if type is '/'
        or '\' respectively.
        """
        rows = self.extract_rows(cells)
        num_rows = len(rows)
        ley_lines = []

        if type_ == '/':
            n = 1
            k = 1
            m = -1
        else:
            n = -1
            k = 2
            m = num_rows

        for i in range(k - 1, self.size + k):
            temp_list = []
            for j in range(max(0, i - k), num_rows - 1):
                temp_list.append(rows[j][i * n])
            if i != (k - 1):
                temp_list.append(rows[num_rows - 1][m + i * n])
            ley_lines.append(temp_list)
        return ley_lines


if __name__ == "__main__":
    from python_ta import check_all
    check_all(config="a2_pyta.txt")
