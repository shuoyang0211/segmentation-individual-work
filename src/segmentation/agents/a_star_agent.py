from typing import Callable

from segmentation_core.engine import GameState, Action, Player


class AStarAgent:
    def __init__(self, side: Player):
        self._name = "A* Agent"
        self._side = side

    @property
    def name(self) -> str:
        return self._name

    @property
    def side(self) -> Player:
        return self._side

    def a_star(self, state: GameState, heuristic: Callable[[GameState], float]):
        """
        Task 3: Implement the A* search algorithm on the game tree to determine
        a sequence of actions that gets your agent to SlothBot.

        Parameters:
            `state`: The current state of the game.
            `heuristic`: A cost-to-go heuristic for game states.

        Note:
            You can assume that SlothBot is stationary and always reachable.
        """
        raise NotImplementedError

    def get_action(self, state: GameState) -> Action:
        """
        Computes the next action to take based on the given game state.

        Parameters:
            `state`: The current state of the game.

        Returns:
            The next action to take to move towards SlothBot.

        Note:
            For your final submission to Gradescope, make sure to use
            squared Euclidean distance as your heuristic function.
        """
        raise NotImplementedError
