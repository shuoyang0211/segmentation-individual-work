from segmentation_core.engine import GameState, Action, Player

class DynamicAStarAgent:
    def __init__(self, side: Player):
        self._name = "Dynamic A* Agent"
        self._side = side

    @property
    def name(self) -> str:
        return self._name

    @property
    def side(self) -> Player:
        return self._side

    def a_star(self, state: GameState):
        raise NotImplementedError

    def get_action(self, state: GameState) -> Action:
        raise NotImplementedError