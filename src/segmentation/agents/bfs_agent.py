from segmentation_core.engine import GameState, Action, Player, Position

class BFSAgent:
    def __init__(self, side: Player):
        self._name = "BFS Agent"
        self._side = side
        self.distance: dict[Position, int] = {}

    @property
    def name(self) -> str:
        return self._name

    @property
    def side(self) -> Player:
        return self._side

    def bfs(self, state: GameState):
        raise NotImplementedError

    def get_action(self, state: GameState) -> Action:
        raise NotImplementedError