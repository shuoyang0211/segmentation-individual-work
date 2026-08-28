from segmentation_core.engine import GameState, Action, Player


class StudentAgent:
    def __init__(self, side: Player):
        self._name = "Student Agent"
        self._side = side

    @property
    def name(self) -> str:
        return self._name

    @property
    def side(self) -> Player:
        return self._side

    def get_action(self, state: GameState) -> Action:
        """
        Computes the next action to take based on the given game state.

        Parameters:
            `state` (`GameState`): The current state of the game.

        Returns:
            Action: The next action to take to move towards SnakeBot.

        Task 4: Return the next action to take based on the given game state to get
        your agent to eliminate SnakeBot.
        """
        raise NotImplementedError
