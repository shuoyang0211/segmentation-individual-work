from segmentation_core.engine import GameState, Action, Player, Position

class DFSAgent():
    def __init__(self, side: Player):
        self._name = "DFS Agent"
        self._side = side
        self.distance: dict[Position, int] = {}

    @property
    def name(self) -> str:
        return self._name

    @property
    def side(self) -> Player:
        return self._side

    def dfs(self, state: GameState):
        raise NotImplementedError

    def get_action(self, state: GameState) -> Action:
        raise NotImplementedError