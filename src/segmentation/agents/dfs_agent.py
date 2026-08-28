from segmentation_core.engine import GameState, Action, Player


class DFSAgent:
    def __init__(self, side: Player):
        self._name = "DFS Agent"
        self._side = side

    @property
    def name(self) -> str:
        return self._name

    @property
    def side(self) -> Player:
        return self._side

    def dfs(self, state: GameState):
        """
        Task 1: Implement depth-first search on the game tree to determine a sequence of actions that gets your agent to SlothBot.

        Note:
            - You can assume that SlothBot is stationary and will always be reachable.
        """
        raise NotImplementedError

    def get_action(self, state: GameState) -> Action:
        """
        Computes the next action to take based on the given game state.

        Parameters:
            `state` (`GameState`): The current state of the game.

        Returns:
            Action: The next action to take to move towards SlothBot.

        Task 1: Return the next action to take based on the given game state to get your agent to SlothBot.
        """
        raise NotImplementedError
