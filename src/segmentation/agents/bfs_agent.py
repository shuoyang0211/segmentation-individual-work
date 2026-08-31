from segmentation_core.engine import Action, GameState, Player


class BFSAgent:
    def __init__(self, side: Player):
        self._name = "BFS Agent"
        self._side = side

    @property
    def name(self) -> str:
        return self._name

    @property
    def side(self) -> Player:
        return self._side

    def bfs(self, state: GameState):
        """
        Task 2: Implement breadth-first search on the game tree to determine
        a sequence of actions that gets your agent to SlothBot.

        Parameters:
            `state`: The current state of the game.

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
        """
        raise NotImplementedError
