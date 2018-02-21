"""
The module used to play our games.
Please fill in the TODO's (i.e. importing games and strategies as needed)

Note: You do not have to run python_ta on this file.
You may import your games from A1 (i.e. Chopsticks). However, the minimax
strategy cannot be used on Chopsticks unless you account for infinite loops.
(You do not have to worry about this for the assignment: only do it for
your own curiousity!)
"""
# TODO: import the modules needed to make game_interface run.
from strategy import *
from typing import Any, Callable
from subtract_square_game import SubtractSquareGame

# TODO: Replace None with the corresponding class name for your games.
# 'h' should map to Stonehenge.
playable_games = {'s': SubtractSquareGame,
                  'h': None}

# TODO: Replace None with the corresponding function names for your strategies.
# 'mr' should map to your recursive implementation of minimax while
# 'mi' should map to your iterative implementation of minimax
usable_strategies = {'i': interactive_strategy,
                     'mr': None,
                     'mi': None}


class GameInterface:
    """
    A game interface for a two-player, sequential move, zero-sum,
    perfect-information game.
    """

    def __init__(self, game: Any, p1_strategy: Callable,
                 p2_strategy: Callable[[Any], Any]) -> None:
        """
        Initialize this GameInterface, setting its active game to game, and
        using the strategies p1_strategy for Player 1 and p2_strategy for
        Player 2.

        :param game: The game to be played.
        :type game:
        :param p1_strategy: The strategy for Player 1.
        :type p1_strategy:
        :param p2_strategy: The strategy for Play 2.
        :type p2_strategy:
        """
        first_player = input("Type y if player 1 is to make the first move: ")
        is_p1_turn = False
        if first_player.lower() == 'y':
            is_p1_turn = True

        self.game = game(is_p1_turn)
        self.p1_strategy = p1_strategy
        self.p2_strategy = p2_strategy

    def play(self) -> None:
        """
        Play the game.
        """
        current_state = self.game.current_state

        print(self.game.get_instructions())
        print(current_state)

        # Pick moves until the game is over
        while not self.game.is_over(current_state):
            move_to_make = None

            # Print out all of the valid moves
            possible_moves = current_state.get_possible_moves()
            print("The current available moves are:")
            for move in possible_moves:
                print(move)

            # Pick a (legal) move.
            while not current_state.is_valid_move(move_to_make):
                current_strategy = self.p2_strategy
                if current_state.get_current_player_name() == 'p1':
                    current_strategy = self.p1_strategy
                move_to_make = current_strategy(self.game)

            # Apply the move
            current_player_name = current_state.get_current_player_name()
            new_game_state = current_state.make_move(move_to_make)
            self.game.current_state = new_game_state
            current_state = self.game.current_state

            print("{} made the move {}. The game's state is now:".format(
                current_player_name, move_to_make))
            print(current_state)

        # Print out the winner of the game
        if self.game.is_winner("p1"):
            print("Player 1 is the winner!")
        elif self.game.is_winner("p2"):
            print("Player 2 is the winner!")
        else:
            print("It's a tie!")


if __name__ == '__main__':
    games = ", ".join(["'{}': {}".format(key, playable_games[key].__name__) if
                       playable_games[key] is not None else
                       "'{}': None".format(key) for key in playable_games])

    strategies = ", ".join(["'{}': {}".format(key,
                                              usable_strategies[key].__name__)
                            if usable_strategies[key] is not None else
                            "'{}': None".format(key)
                            for key in usable_strategies])

    chosen_game = ''
    while chosen_game not in playable_games.keys():
        chosen_game = input(
            "Select the game you want to play ({}): ".format(games))

    p1 = ''
    p2 = ''

    while p1 not in usable_strategies.keys():
        p1 = input("Select the strategy for Player 1 ({}): ".format(strategies))

    while p2 not in usable_strategies.keys():
        p2 = input("Select the strategy for Player 2 ({}): ".format(strategies))

    GameInterface(playable_games[chosen_game], usable_strategies[p1],
                  usable_strategies[p2]).play()
