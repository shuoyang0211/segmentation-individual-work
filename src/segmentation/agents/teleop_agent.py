import pygame

from segmentation_core.engine import GameState, Action, Player


class TeleopAgent:
    def __init__(self, side: Player) -> None:
        self._name = "Teleop Agent"
        self._side = side

        if not pygame.get_init():
            pygame.init()

    @property
    def name(self) -> str:
        return self._name

    @property
    def side(self) -> Player:
        return self._side

    def _from_key(self, key: int) -> Action | None:
        if key == pygame.K_SPACE:
            return Action.STAY
        if key in (pygame.K_w, pygame.K_UP):
            return Action.UP
        if key in (pygame.K_s, pygame.K_DOWN):
            return Action.DOWN
        if key in (pygame.K_a, pygame.K_LEFT):
            return Action.LEFT
        if key in (pygame.K_d, pygame.K_RIGHT):
            return Action.RIGHT
        return None

    def get_action(self, state: GameState) -> Action:
        while True:
            event = pygame.event.wait()

            if event.type == pygame.QUIT:
                raise SystemExit

            if event.type == pygame.KEYDOWN:
                act = self._from_key(event.key)
                if act is not None:
                    return act

            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    raise SystemExit
                if e.type == pygame.KEYDOWN:
                    act = self._from_key(e.key)
                    if act is not None:
                        return act
