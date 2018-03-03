"""
A module for strategies.

NOTE: Make sure this file adheres to python-ta.
Adjust the type annotations as needed, and implement both a recursive
and an iterative version of minimax.
"""

from typing import Any, Optional
from game import Game
from game_state import GameState


class TreeNode:
    """
    A bare-bones Tree ADT that identifies the root with the entire tree.
    """

    def __init__(self, value: GameState, children: Optional[GameState] = None,
                 score: Optional[int] = None) -> None:
        """
        Create Tree self with content value and 0 or more children
        """
        self.value = value
        self.children = children[:] if children is not None else []
        self.score = score


class Stack:
    """ Last-in, first-out (LIFO) stack.
    """

    def __init__(self) -> None:
        """ Create a new, empty Stack self.

        >>> s = Stack()
        """
        self._contains = []

    def add(self, obj: TreeNode) -> None:
        """ Add object obj to top of Stack self.

        >>> s = Stack()
        >>> s.add(5)
        """
        self._contains.append(obj)

    def remove(self) -> TreeNode:
        """
        Remove and return top element of Stack self.

        Assume Stack self is not emp.

        >>> s = Stack()
        >>> s.add(5)
        >>> s.add(7)
        >>> s.remove()
        7
        """
        return self._contains.pop()

    def is_empty(self) -> bool:
        """
        Return whether Stack self is empty.

        >>> s = Stack()
        >>> s.is_empty()
        True
        >>> s.add(5)
        >>> s.is_empty()
        False
        """
        return len(self._contains) == 0


# TODO: Adjust the type annotation as needed.
def interactive_strategy(game: Game) -> Any:
    """
    Return a move for game through interactively asking the user for input.
    """
    move = input("Enter a move: ")
    return game.str_to_move(move)


def rough_outcome_strategy(game: Any) -> Any:
    """
    Return a move for game by picking a move which results in a state with
    the lowest rough_outcome() for the opponent.

    NOTE: game.rough_outcome() should do the following:
        - For a state that's over, it returns the score for the current
          player of that state.
        - For a state that's not over:
            - If there is a move that results in the current player winning,
              return 1.
            - If all moves result in states where the other player can
              immediately win, return -1.
            - Otherwise; return a number between -1 and 1 corresponding to how
              'likely' the current player will win from the current state.

        In essence: rough_outcome() will only look 1 or 2 states ahead to
        'guess' the outcome of the game, but no further. It's better than
        random, but worse than minimax.
    """
    current_state = game.current_state
    best_move = None
    best_outcome = -2  # Temporarily -- just so we can replace this easily later

    # Get the move that results in the lowest rough_outcome for the opponent
    for move in current_state.get_possible_moves():
        new_state = current_state.make_move(move)

        # We multiply the below by -1 since a state that's bad for the opponent
        # is good for us.
        guessed_score = new_state.rough_outcome() * -1
        if guessed_score > best_outcome:
            best_outcome = guessed_score
            best_move = move

    # Return the move that resulted in the best rough_outcome
    return best_move


# TODO: Implement a recursive version of the minimax strategy.
def minimax_strategy_r(game: Any) -> Any:
    """
    Return a move for game by using recursive minimax.
    """
    moves = game.current_state.get_possible_moves()
    scores = [get_score(game, game.current_state.make_move(move)) for move in
              moves]
    return moves[scores.index(min(scores))]


def get_score(game: Game, state: GameState) -> int:
    """
    Get all the scores for the possible moves.
    """
    curr_state = game.current_state

    if state.p1_turn:
        current_player = 'p1'
        other_player = 'p2'
    else:
        current_player = 'p2'
        other_player = 'p1'

    if game.is_over(state):
        game.current_state = state
        if game.is_winner(current_player):
            game.current_state = curr_state
            return 1
        elif game.is_winner(other_player):
            game.current_state = curr_state
            return -1
        game.current_state = curr_state
        return 0
    a = [get_score(game, state.make_move(move)) for move in
         state.get_possible_moves()]
    return max([-1 * score for score in a])


# TODO: Implement an iterative version of the minimax strategy.
def minimax_strategy_i(game: Game) -> Any:
    """
    Return a move for game by using iterative minimax.
    """
    curr_state = game.current_state
    top_node = TreeNode(curr_state)
    s = Stack()
    s.add(top_node)
    while not s.is_empty():
        removed_node = s.remove()
        state = removed_node.value
        if game.is_over(state):
            if state.p1_turn:
                current_player = 'p1'
                other_player = 'p2'
            else:
                current_player = 'p2'
                other_player = 'p1'

            game.current_state = state
            if game.is_winner(current_player):
                removed_node.score = 1
            elif game.is_winner(other_player):
                removed_node.score = -1
            else:
                removed_node.score = 0
            game.current_state = curr_state
        elif removed_node.children == []:
            s.add(removed_node)
            for move in state.get_possible_moves():
                child_node = TreeNode(state.make_move(move))
                removed_node.children.append(child_node)
                s.add(child_node)
        else:
            removed_node.score = max([-1 * child.score for child in
                                      removed_node.children])
    moves = curr_state.get_possible_moves()
    child_scores = [child.score for child in top_node.children]
    return moves[child_scores.index(top_node.score * -1)]


if __name__ == "__main__":
    from python_ta import check_all
    check_all(config="a2_pyta.txt")
